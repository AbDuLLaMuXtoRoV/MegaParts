"""Admin login: one configured account, a signed session cookie, and brute-force throttling.

The cookie is ``username|expires|signature``. The signing key mixes SESSION_SECRET with the
admin password, so changing ADMIN_PASSWORD signs every existing session out.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets
import time
from collections import defaultdict, deque

from app.config import Settings

COOKIE_NAME = "megaparts_admin"
MAX_FAILED_LOGINS = 5
FAILED_LOGIN_WINDOW_SECONDS = 15 * 60

# Without SESSION_SECRET, sessions are valid only until the server restarts.
_fallback_secret = secrets.token_hex(32)


def is_admin_path(path: str) -> bool:
    if path in {"/admin/login", "/api/admin/login", "/api/admin/logout"}:
        return False
    return path == "/admin" or path.startswith(("/admin/", "/api/admin/"))


def _signing_key(settings: Settings) -> bytes:
    secret = settings.session_secret or _fallback_secret
    return hashlib.sha256(f"{secret}\x00{settings.admin_password}".encode()).digest()


def _signature(settings: Settings, payload: str) -> str:
    return hmac.new(_signing_key(settings), payload.encode(), hashlib.sha256).hexdigest()


def issue_session(settings: Settings, now: float | None = None) -> str:
    expires = int((now or time.time()) + settings.admin_session_hours * 3600)
    payload = f"{settings.admin_username}|{expires}"
    return f"{payload}|{_signature(settings, payload)}"


def session_user(settings: Settings, cookie: str | None, now: float | None = None) -> str | None:
    if not cookie or not settings.admin_password:
        return None
    try:
        username, expires, signature = cookie.rsplit("|", 2)
        expires_at = int(expires)
    except ValueError:
        return None
    expected = _signature(settings, f"{username}|{expires}")
    if not hmac.compare_digest(signature.encode(), expected.encode()):
        return None
    if expires_at < (now or time.time()) or username != settings.admin_username:
        return None
    return username


def credentials_match(settings: Settings, username: str, password: str) -> bool:
    # Compare both fields every time so timing does not reveal which one was wrong.
    user_ok = hmac.compare_digest(username.encode(), settings.admin_username.encode())
    password_ok = hmac.compare_digest(password.encode(), settings.admin_password.encode())
    return bool(settings.admin_password) and user_ok and password_ok


class LoginThrottle:
    """In-memory per-client limit on failed logins (single-process deployments)."""

    def __init__(self) -> None:
        self._failures: dict[str, deque[float]] = defaultdict(deque)

    def _recent(self, key: str, now: float) -> deque[float]:
        failures = self._failures[key]
        while failures and failures[0] <= now - FAILED_LOGIN_WINDOW_SECONDS:
            failures.popleft()
        return failures

    def retry_after(self, key: str, now: float | None = None) -> int:
        now = now or time.time()
        failures = self._recent(key, now)
        if len(failures) < MAX_FAILED_LOGINS:
            return 0
        return max(1, int(failures[0] + FAILED_LOGIN_WINDOW_SECONDS - now))

    def fail(self, key: str, now: float | None = None) -> None:
        self._recent(key, now or time.time()).append(now or time.time())

    def reset(self, key: str) -> None:
        self._failures.pop(key, None)
