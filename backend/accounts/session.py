from datetime import datetime, timedelta

from django.contrib.auth import logout as auth_logout
from django.utils import timezone


SESSION_LOGOUT_AT_KEY = "session_logout_at"


def next_local_midnight(now=None):
    current = timezone.localtime(now or timezone.now())
    return (current + timedelta(days=1)).replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )


def _parse_deadline(raw_value):
    if not raw_value:
        return None
    try:
        parsed = datetime.fromisoformat(str(raw_value))
    except ValueError:
        return None
    if timezone.is_naive(parsed):
        return timezone.make_aware(parsed, timezone.get_current_timezone())
    return parsed


def ensure_session_deadline(request, *, reset=False):
    if not getattr(request.user, "is_authenticated", False):
        return None

    deadline = None if reset else _parse_deadline(request.session.get(SESSION_LOGOUT_AT_KEY))
    if deadline is None:
        deadline = next_local_midnight()
        request.session[SESSION_LOGOUT_AT_KEY] = deadline.isoformat()
        request.session.modified = True
    return deadline


def enforce_session_deadline(request):
    deadline = ensure_session_deadline(request)
    if deadline and timezone.now() >= deadline:
        auth_logout(request)
        return None
    return deadline
