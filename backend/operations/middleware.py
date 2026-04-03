import uuid

from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from .services import capture_exception


class RequestContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.request_id = request.META.get("HTTP_X_REQUEST_ID") or uuid.uuid4().hex
        response = self.get_response(request)
        response["X-Request-ID"] = request.request_id

        user = getattr(request, "user", None)
        if getattr(user, "is_authenticated", False):
            previous_seen = user.last_seen_at
            now = timezone.now()
            user_pk = getattr(user, "pk", None)
            if user_pk and (
                previous_seen is None or (now - previous_seen).total_seconds() >= 300
            ):
                get_user_model().objects.filter(pk=user_pk).update(last_seen_at=now)
                user.last_seen_at = now

        return response


class SecurityHeadersMiddleware:
    _NO_STORE_PATHS = {
        "/",
        "/index.html",
        "/login.html",
        "/access-denied.html",
        "/admin-console.html",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        csp_policy = str(getattr(settings, "CONTENT_SECURITY_POLICY", "")).strip()
        if csp_policy and "Content-Security-Policy" not in response:
            response["Content-Security-Policy"] = csp_policy

        permissions_policy = str(getattr(settings, "PERMISSIONS_POLICY", "")).strip()
        if permissions_policy and "Permissions-Policy" not in response:
            response["Permissions-Policy"] = permissions_policy

        if self._should_disable_caching(request.path):
            response["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
            response["Pragma"] = "no-cache"
            response["Expires"] = "0"

        return response

    @staticmethod
    def _should_disable_caching(path):
        normalized = str(path or "").strip() or "/"
        if normalized.startswith("/api/"):
            return True
        return normalized in SecurityHeadersMiddleware._NO_STORE_PATHS


class ErrorMonitoringMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        capture_exception(exception, request=request)
        return None
