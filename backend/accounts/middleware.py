from .session import enforce_session_deadline


class SessionDeadlineMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        enforce_session_deadline(request)
        return self.get_response(request)
