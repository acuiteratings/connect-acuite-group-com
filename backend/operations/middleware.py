import uuid

from django.contrib.auth import get_user_model
from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone

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


class ErrorMonitoringMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        capture_exception(exception, request=request)
        return None
