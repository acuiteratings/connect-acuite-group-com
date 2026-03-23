import traceback as traceback_module

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from .models import AnalyticsEvent, AuditLog, ErrorEvent


def _request_ip(request):
    if request is None:
        return None
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def _request_user_agent(request):
    if request is None:
        return ""
    return request.META.get("HTTP_USER_AGENT", "")


def _request_id(request):
    if request is None:
        return ""
    return getattr(request, "request_id", "") or request.META.get("HTTP_X_REQUEST_ID", "")


def record_audit_event(action, summary, actor=None, target=None, metadata=None, request=None):
    target_content_type = None
    target_object_id = ""
    if target is not None:
        target_content_type = ContentType.objects.get_for_model(
            target,
            for_concrete_model=False,
        )
        target_object_id = str(target.pk)

    return AuditLog.objects.create(
        actor=actor if getattr(actor, "is_authenticated", False) else None,
        action=action,
        summary=summary,
        target_content_type=target_content_type,
        target_object_id=target_object_id,
        request_id=_request_id(request),
        metadata=metadata or {},
        ip_address=_request_ip(request),
        user_agent=_request_user_agent(request),
    )


def record_analytics_event(category, event_name, actor=None, path="", metadata=None, request=None):
    resolved_path = path or (request.path if request else "")
    return AnalyticsEvent.objects.create(
        actor=actor if getattr(actor, "is_authenticated", False) else None,
        category=category,
        event_name=event_name,
        request_id=_request_id(request),
        path=resolved_path,
        metadata=metadata or {},
        ip_address=_request_ip(request),
        user_agent=_request_user_agent(request),
    )


def record_error_event(
    exception_type,
    message,
    *,
    actor=None,
    request=None,
    status_code=500,
    metadata=None,
    traceback_text="",
):
    return ErrorEvent.objects.create(
        actor=actor if getattr(actor, "is_authenticated", False) else None,
        request_id=_request_id(request),
        path=(request.path if request else ""),
        method=(request.method if request else ""),
        status_code=status_code,
        exception_type=exception_type,
        message=message,
        traceback=traceback_text,
        metadata=metadata or {},
        ip_address=_request_ip(request),
        user_agent=_request_user_agent(request),
    )


def capture_exception(exc, request=None):
    traceback_text = "".join(
        traceback_module.format_exception(type(exc), exc, exc.__traceback__)
    )[:12000]
    return record_error_event(
        type(exc).__name__,
        str(exc) or type(exc).__name__,
        actor=getattr(request, "user", None),
        request=request,
        status_code=500,
        metadata={"captured_at": timezone.now().isoformat()},
        traceback_text=traceback_text,
    )
