#!/usr/bin/env python3
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen


BASE_URL = os.getenv("PRODUCTION_URL", "https://connect.acuite-group.com").rstrip("/")
BASE_URL_PARTS = urlparse(BASE_URL)
if BASE_URL_PARTS.scheme != "https" or not BASE_URL_PARTS.netloc:
    raise RuntimeError("PRODUCTION_URL must be an HTTPS URL.")
EXPECTED_COMMIT = os.getenv("EXPECTED_COMMIT", "").strip()
TIMEOUT_SECONDS = int(os.getenv("SMOKE_TIMEOUT_SECONDS", "900"))
POLL_SECONDS = int(os.getenv("SMOKE_POLL_SECONDS", "20"))

PROTECTED_ENDPOINTS = (
    "/api/directory/",
    "/api/feed/posts/",
    "/api/learning/books/",
    "/api/store/overview/",
    "/api/recognition/overview/",
    "/api/voice/polls/active/",
)
PUBLIC_ENDPOINTS = (
    "/api/accounts/me/",
    "/api/ops/health/",
)


def _request(path, *, read_body=True):
    query = urlencode({"_smoke": str(time.time_ns())})
    separator = "&" if "?" in path else "?"
    url = f"{BASE_URL}{path}{separator}{query}"
    request = Request(
        url,
        headers={
            "Accept": "application/json,text/html",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "Connection": "close",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:  # nosec B310
            body = response.read() if read_body else b""
            return response.status, body, dict(response.headers)
    except HTTPError as exc:
        body = exc.read() if read_body else b""
        return exc.code, body, dict(exc.headers)


def _json_body(body):
    try:
        return json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}


def _login_build_number():
    status, body, _headers = _request("/login.html")
    if status != 200:
        raise RuntimeError(f"login page returned HTTP {status}")
    text = body.decode("utf-8", errors="replace")
    matches = re.findall(r"BUILD\s*([0-9.]+)", text, flags=re.I)
    return matches[-1] if matches else "unknown"


def _health_payload():
    status, body, _headers = _request("/api/ops/health/")
    if status != 200:
        raise RuntimeError(f"health endpoint returned HTTP {status}")
    return _json_body(body)


def _wait_for_expected_commit():
    deadline = time.time() + TIMEOUT_SECONDS
    last_seen = ""
    while True:
        health = _health_payload()
        last_seen = str(health.get("commit_sha") or "").strip()
        if not EXPECTED_COMMIT or last_seen.startswith(EXPECTED_COMMIT[:12]):
            return health
        if time.time() >= deadline:
            raise RuntimeError(
                f"Timed out waiting for deployed commit {EXPECTED_COMMIT}; last seen {last_seen or 'unknown'}."
            )
        print(
            f"{datetime.now(timezone.utc).isoformat()} waiting for deploy; "
            f"last seen commit={last_seen or 'unknown'}",
            flush=True,
        )
        time.sleep(POLL_SECONDS)


def main():
    try:
        health = _wait_for_expected_commit()
        build_number = _login_build_number()
        print(
            f"Production health ok: build={health.get('build_number') or build_number} "
            f"commit={health.get('commit_sha') or 'unknown'}"
        )

        failures = []
        for path in PROTECTED_ENDPOINTS:
            status, body, _headers = _request(path)
            if status != 403:
                failures.append(f"{path} expected 403, got {status} ({len(body)} bytes)")

        for path in PUBLIC_ENDPOINTS:
            status, body, _headers = _request(path)
            if status != 200:
                failures.append(f"{path} expected 200, got {status} ({len(body)} bytes)")

        if failures:
            raise RuntimeError("; ".join(failures))
    except (RuntimeError, URLError) as exc:
        print(f"Production smoke check failed: {exc}", file=sys.stderr)
        return 1

    print("Production smoke check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
