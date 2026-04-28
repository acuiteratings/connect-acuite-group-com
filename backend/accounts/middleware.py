from django.http import JsonResponse

from .session import enforce_session_deadline


class EmployeeApiAccessMiddleware:
    PUBLIC_API_PATH_PREFIXES = (
        "/api/accounts/auth/",
    )
    PUBLIC_API_PATHS = {
        "/api/accounts/me/",
        "/api/ops/health/",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        forbidden = self._employee_access_required_response(request)
        if forbidden:
            return forbidden
        return self.get_response(request)

    def _employee_access_required_response(self, request):
        path = request.path_info or request.path or ""
        if not path.startswith("/api/"):
            return None
        if path in self.PUBLIC_API_PATHS:
            return None
        if any(path.startswith(prefix) for prefix in self.PUBLIC_API_PATH_PREFIXES):
            return None

        user = getattr(request, "user", None)
        if getattr(user, "is_authenticated", False) and getattr(user, "has_employee_access", False):
            return None
        return JsonResponse(
            {"detail": "Authentication required."},
            status=403,
        )


class SessionDeadlineMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        enforce_session_deadline(request)
        return self.get_response(request)
