"""Vercel Python serverless function: read-only Redis inspector.

Lets the team see what is actually in the Upstash store behind the datadump
and comments features. Read-only by design — no delete/write endpoints.

Only keys under the app's own prefixes are visible: `dump:*` and `comments:*`.

Endpoints:
  GET /api/dbview             -> { "keys": [ {key, type, items?, bytes?}, ... ],
                                   "totals": {keys, media, media_bytes} }
  GET /api/dbview?key=<key>   -> contents of one key:
        list   -> { key, type: "list", count, items: [parsed JSON or raw string] }
        media  -> { key, type: "media", mime, approx_bytes, media_id }
        string -> { key, type: "string", value (truncated at 100 KB) }

Required env vars: same as comments.py (KV_REST_API_URL/TOKEN or UPSTASH_*).
"""

import json
import os
import urllib.request
from http.server import BaseHTTPRequestHandler

VISIBLE_PREFIXES = ("dump:", "comments:")
MAX_VALUE_LEN = 100_000


def _redis_creds():
    url = os.environ.get("KV_REST_API_URL") or os.environ.get("UPSTASH_REDIS_REST_URL")
    token = os.environ.get("KV_REST_API_TOKEN") or os.environ.get("UPSTASH_REDIS_REST_TOKEN")
    return url, token


def _request(path, payload):
    url, token = _redis_creds()
    if not url or not token:
        raise RuntimeError("Redis credentials not configured (KV_REST_API_URL / KV_REST_API_TOKEN)")
    req = urllib.request.Request(
        url.rstrip("/") + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _redis(command):
    payload = _request("/", command)
    if isinstance(payload, dict) and payload.get("error"):
        raise RuntimeError("Redis error: " + str(payload["error"]))
    return payload.get("result") if isinstance(payload, dict) else payload


def _pipeline(commands):
    """Run many commands in one round-trip. Returns list of results (None on per-command error)."""
    if not commands:
        return []
    payload = _request("/pipeline", commands)
    out = []
    for item in payload:
        if isinstance(item, dict) and item.get("error"):
            out.append(None)
        else:
            out.append(item.get("result") if isinstance(item, dict) else item)
    return out


def _visible(key):
    return isinstance(key, str) and key.startswith(VISIBLE_PREFIXES)


def scan_keys():
    keys = []
    for prefix in VISIBLE_PREFIXES:
        cursor = "0"
        for _ in range(50):  # hard bound on rounds
            res = _redis(["SCAN", cursor, "MATCH", prefix + "*", "COUNT", "1000"])
            cursor, batch = str(res[0]), res[1] or []
            keys.extend(batch)
            if cursor == "0":
                break
    return sorted(set(k for k in keys if _visible(k)))


def overview():
    keys = scan_keys()
    types = _pipeline([["TYPE", k] for k in keys])
    size_cmds = []
    for k, t in zip(keys, types):
        size_cmds.append(["LLEN", k] if t == "list" else ["STRLEN", k])
    sizes = _pipeline(size_cmds)

    rows, media_count, media_bytes = [], 0, 0
    for k, t, s in zip(keys, types, sizes):
        row = {"key": k, "type": t}
        if t == "list":
            row["items"] = s or 0
        else:
            # STRLEN of the stored JSON wrapper; close enough for a storage overview
            row["bytes"] = s or 0
            if k.startswith("dump:media:"):
                media_count += 1
                media_bytes += s or 0
        rows.append(row)
    return {
        "keys": rows,
        "totals": {"keys": len(rows), "media": media_count, "media_bytes": media_bytes},
    }


def detail(key):
    """Return (status, payload) for one key."""
    if not _visible(key):
        return 400, {"error": "key outside visible prefixes (dump:*, comments:*)"}
    t = _redis(["TYPE", key])
    if t in (None, "none"):
        return 404, {"error": "key not found"}
    if t == "list":
        raw = _redis(["LRANGE", key, "0", "-1"]) or []
        items = []
        for item in raw:
            try:
                items.append(json.loads(item))
            except (ValueError, TypeError):
                items.append(item)
        return 200, {"key": key, "type": "list", "count": len(items), "items": items}
    if t == "string":
        raw = _redis(["GET", key]) or ""
        if key.startswith("dump:media:"):
            try:
                obj = json.loads(raw)
                b64_len = len(obj.get("b64", ""))
                return 200, {
                    "key": key,
                    "type": "media",
                    "mime": obj.get("mime"),
                    "approx_bytes": (b64_len * 3) // 4,
                    "media_id": key.rsplit(":", 1)[1],
                }
            except (ValueError, TypeError):
                pass
        return 200, {
            "key": key,
            "type": "string",
            "value": raw[:MAX_VALUE_LEN],
            "truncated": len(raw) > MAX_VALUE_LEN,
        }
    return 200, {"key": key, "type": t}


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
        key = (qs.get("key") or [None])[0]
        try:
            if key:
                status, payload = detail(key)
                return self._send_json(status, payload)
            return self._send_json(200, overview())
        except Exception as exc:  # noqa: BLE001 - surface config/store errors to client
            return self._send_json(500, {"error": str(exc)})
