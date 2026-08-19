"""Vercel Python serverless function: persistent RFC comments.

Storage: Upstash Redis (provisioned via Vercel Marketplace). Comments for a
page live in a Redis list under the key `comments:<page>`; each element is a
JSON-encoded comment object. Reads use LRANGE, writes use RPUSH — always fresh,
no filesystem needed (Vercel's FS is read-only / ephemeral).

Endpoints (same origin as the site):
  GET  /api/comments?page=<slug>   -> { "comments": [ {id, author, body, ts}, ... ] }
  POST /api/comments               -> body { page, author, body }; returns the stored comment

Required env vars (auto-injected by the Vercel Upstash integration; both the
KV_* and UPSTASH_* names are accepted):
  KV_REST_API_URL    / UPSTASH_REDIS_REST_URL
  KV_REST_API_TOKEN  / UPSTASH_REDIS_REST_TOKEN
"""

import json
import os
import re
import time
import uuid
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler

# Only these pages may be commented on (matches the RFC tab in index.html).
# Entries without ".html" are per-section thread slugs (data-comments attributes).
ALLOWED_PAGES = {
    "sim-design-discussion.html",
    "bus-and-digital-twin.html",
    "digital-twin-flow.html",
    "wrc-2026.html",
    "wrc-2026-omni-base",
    "wrc-2026-area-gripper",
}

MAX_BODY_LEN = 5000
MAX_AUTHOR_LEN = 80
MAX_COMMENTS = 1000  # safety cap per page


def _redis_creds():
    url = os.environ.get("KV_REST_API_URL") or os.environ.get("UPSTASH_REDIS_REST_URL")
    token = os.environ.get("KV_REST_API_TOKEN") or os.environ.get("UPSTASH_REDIS_REST_TOKEN")
    return url, token


def _redis(command):
    """Run a single Redis command via the Upstash REST API. Returns `result`."""
    url, token = _redis_creds()
    if not url or not token:
        raise RuntimeError("Redis credentials not configured (KV_REST_API_URL / KV_REST_API_TOKEN)")
    req = urllib.request.Request(
        url.rstrip("/") + "/",
        data=json.dumps(command).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if isinstance(payload, dict) and payload.get("error"):
        raise RuntimeError("Redis error: " + str(payload["error"]))
    return payload.get("result") if isinstance(payload, dict) else payload


def _clean_page(page):
    """Normalise to a bare filename and verify it's an allowed RFC page."""
    if not page:
        return None
    page = page.strip().split("/")[-1].split("?")[0]
    if not re.fullmatch(r"[a-z0-9._-]+", page):
        return None
    return page if page in ALLOWED_PAGES else None


def _key(page):
    return "comments:" + page


def _get_comments(page):
    raw = _redis(["LRANGE", _key(page), "0", "-1"]) or []
    out = []
    for item in raw:
        try:
            out.append(json.loads(item))
        except (ValueError, TypeError):
            continue
    return out


class handler(BaseHTTPRequestHandler):
    def _send(self, status, obj):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        from urllib.parse import urlparse, parse_qs
        qs = parse_qs(urlparse(self.path).query)
        page = _clean_page((qs.get("page") or [None])[0])
        if not page:
            return self._send(400, {"error": "unknown or missing page"})
        try:
            comments = _get_comments(page)
        except Exception as exc:  # noqa: BLE001 - surface config/store errors to client
            return self._send(500, {"error": str(exc)})
        return self._send(200, {"comments": comments})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            data = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
        except (ValueError, TypeError):
            return self._send(400, {"error": "invalid JSON body"})

        page = _clean_page(data.get("page"))
        if not page:
            return self._send(400, {"error": "unknown or missing page"})

        author = (data.get("author") or "").strip()[:MAX_AUTHOR_LEN] or "Anonymous"
        text = (data.get("body") or "").strip()[:MAX_BODY_LEN]
        if not text:
            return self._send(400, {"error": "comment body is empty"})

        comment = {
            "id": uuid.uuid4().hex,
            "author": author,
            "body": text,
            "ts": int(time.time() * 1000),
        }
        try:
            _redis(["RPUSH", _key(page), json.dumps(comment)])
            # Trim to the most recent MAX_COMMENTS to bound storage.
            _redis(["LTRIM", _key(page), str(-MAX_COMMENTS), "-1"])
        except Exception as exc:  # noqa: BLE001
            return self._send(500, {"error": str(exc)})

        return self._send(201, {"comment": comment})
