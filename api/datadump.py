"""Vercel Python serverless function: conference "datadump" feed.

A phone-first shared feed: text notes, photos and voice memos dumped from the
expo floor land in one chronological album that the whole team can read.

Storage: same Upstash Redis as api/comments.py.
  dump:<album>:entries   Redis list of JSON entry metadata (RPUSH/LRANGE)
  dump:media:<id>        JSON string {"mime": ..., "b64": ...} per media blob

Endpoints:
  GET  /api/datadump?album=<slug>      -> { "entries": [ {id, author, kind, body, tag, mime, ts}, ... ] }
  GET  /api/datadump?media=<id>        -> raw media bytes (Content-Type from stored mime, immutable cache)
  POST /api/datadump                   -> body { album, author, kind, body?, tag?, mime?, data? (base64) }
                                          kind: "text" | "image" | "audio"

Media is stored base64 in Redis; clients MUST compress before upload
(datadump.html targets <= ~700 KB binary per item). Request size guard below.

Required env vars: same as comments.py (KV_REST_API_URL/TOKEN or UPSTASH_*).
"""

import base64
import json
import os
import re
import time
import uuid
import urllib.request
from http.server import BaseHTTPRequestHandler

ALLOWED_ALBUMS = {"wrc-2026"}
ALLOWED_KINDS = {"text", "image", "audio"}
ALLOWED_MIMES = {
    "image/jpeg", "image/png", "image/webp",
    "audio/mp4", "audio/mpeg", "audio/webm", "audio/webm;codecs=opus", "audio/ogg",
}
MAX_B64_LEN = 1_400_000   # ~1.0 MB binary after decode
MAX_BODY_LEN = 10_000
MAX_AUTHOR_LEN = 80
MAX_TAG_LEN = 120
MAX_ENTRIES = 2000


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
    with urllib.request.urlopen(req, timeout=15) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    if isinstance(payload, dict) and payload.get("error"):
        raise RuntimeError("Redis error: " + str(payload["error"]))
    return payload.get("result") if isinstance(payload, dict) else payload


def _clean_album(album):
    if not album:
        return None
    album = album.strip()
    if not re.fullmatch(r"[a-z0-9-]+", album):
        return None
    return album if album in ALLOWED_ALBUMS else None


def _entries_key(album):
    return "dump:" + album + ":entries"


def _media_key(media_id):
    return "dump:media:" + media_id


def list_entries(album):
    raw = _redis(["LRANGE", _entries_key(album), "0", "-1"]) or []
    out = []
    for item in raw:
        try:
            out.append(json.loads(item))
        except (ValueError, TypeError):
            continue
    return out


def get_media(media_id):
    """Return (bytes, mime) or (None, None)."""
    if not re.fullmatch(r"[a-f0-9]{32}", media_id or ""):
        return None, None
    raw = _redis(["GET", _media_key(media_id)])
    if not raw:
        return None, None
    try:
        obj = json.loads(raw)
        return base64.b64decode(obj["b64"]), obj.get("mime") or "application/octet-stream"
    except (ValueError, TypeError, KeyError):
        return None, None


def add_entry(data):
    """Validate + store one entry. Returns (status, payload)."""
    album = _clean_album(data.get("album"))
    if not album:
        return 400, {"error": "unknown or missing album"}

    kind = (data.get("kind") or "").strip()
    if kind not in ALLOWED_KINDS:
        return 400, {"error": "kind must be text, image or audio"}

    author = (data.get("author") or "").strip()[:MAX_AUTHOR_LEN] or "Anonymous"
    body = (data.get("body") or "").strip()[:MAX_BODY_LEN]
    tag = (data.get("tag") or "").strip()[:MAX_TAG_LEN]

    entry = {
        "id": uuid.uuid4().hex,
        "author": author,
        "kind": kind,
        "body": body,
        "tag": tag,
        "ts": int(time.time() * 1000),
    }

    if kind == "text":
        if not body:
            return 400, {"error": "text entry needs a body"}
    else:
        b64 = data.get("data") or ""
        mime = (data.get("mime") or "").split(";")[0].strip().lower()
        full_mime = (data.get("mime") or "").strip().lower()
        if full_mime not in ALLOWED_MIMES and mime not in ALLOWED_MIMES:
            return 400, {"error": "unsupported mime type: " + (data.get("mime") or "(none)")}
        if not b64:
            return 400, {"error": "media entry needs base64 data"}
        if len(b64) > MAX_B64_LEN:
            return 413, {"error": "media too large — compress below ~1 MB"}
        try:
            base64.b64decode(b64, validate=True)
        except Exception:
            return 400, {"error": "data is not valid base64"}
        entry["mime"] = mime or full_mime
        _redis(["SET", _media_key(entry["id"]), json.dumps({"mime": entry["mime"], "b64": b64})])

    _redis(["RPUSH", _entries_key(album), json.dumps(entry)])
    _redis(["LTRIM", _entries_key(album), str(-MAX_ENTRIES), "-1"])
    return 201, {"entry": entry}


class handler(BaseHTTPRequestHandler):
    def _send_json(self, status, obj):
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

        media_id = (qs.get("media") or [None])[0]
        if media_id:
            try:
                blob, mime = get_media(media_id)
            except Exception as exc:  # noqa: BLE001
                return self._send_json(500, {"error": str(exc)})
            if blob is None:
                return self._send_json(404, {"error": "media not found"})
            self.send_response(200)
            self.send_header("Content-Type", mime)
            self.send_header("Content-Length", str(len(blob)))
            # media blobs are immutable per id — let the phone cache them
            self.send_header("Cache-Control", "public, max-age=31536000, immutable")
            self.end_headers()
            self.wfile.write(blob)
            return

        album = _clean_album((qs.get("album") or [None])[0])
        if not album:
            return self._send_json(400, {"error": "unknown or missing album"})
        try:
            entries = list_entries(album)
        except Exception as exc:  # noqa: BLE001
            return self._send_json(500, {"error": str(exc)})
        return self._send_json(200, {"entries": entries})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length") or 0)
            data = json.loads(self.rfile.read(length).decode("utf-8")) if length else {}
        except (ValueError, TypeError):
            return self._send_json(400, {"error": "invalid JSON body"})
        try:
            status, payload = add_entry(data)
        except Exception as exc:  # noqa: BLE001
            return self._send_json(500, {"error": str(exc)})
        return self._send_json(status, payload)
