from .services import capture_attendance_activity


class AttendanceCaptureMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if request.path_info.startswith("/api/") and getattr(user, "is_authenticated", False):
            source = "logout" if request.path_info == "/api/accounts/auth/logout/" else "activity"
            capture_attendance_activity(request, source=source)
        return self.get_response(request)
