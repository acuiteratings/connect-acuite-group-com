from .services import capture_attendance_activity


class AttendanceCaptureMiddleware:
    TRACKED_API_PATHS = {
        "/api/accounts/me/",
        "/api/attendance/status/",
        "/api/accounts/auth/logout/",
    }

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if (
            request.path_info in self.TRACKED_API_PATHS
            and getattr(user, "is_authenticated", False)
        ):
            source = "logout" if request.path_info == "/api/accounts/auth/logout/" else "activity"
            capture_attendance_activity(request, source=source)
        return self.get_response(request)
