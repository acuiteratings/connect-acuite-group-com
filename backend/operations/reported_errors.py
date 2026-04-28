from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from accounts.models import User

from .models import ReportedError
from .serializers import serialize_reported_error
from .services import record_audit_event


def _is_admin_user(user):
    return user.is_authenticated and (
        user.is_staff
        or getattr(user, "can_administer_connect", False)
        or getattr(user, "access_level", "") == User.AccessLevel.ADMIN
        or user.has_perm("accounts.manage_access_rights")
    )


def _forbidden():
    return JsonResponse({"detail": "Admin access required."}, status=403)


def reported_errors_admin_collection(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    if not _is_admin_user(request.user):
        return _forbidden()

    queryset = ReportedError.objects.select_related("reporter", "resolved_by")
    results = [serialize_reported_error(event) for event in queryset]
    return JsonResponse({"count": len(results), "results": results})


def reported_error_admin_resolve(request, reported_error_id):
    if request.method != "PATCH":
        return HttpResponseNotAllowed(["PATCH"])
    if not _is_admin_user(request.user):
        return _forbidden()

    event = get_object_or_404(
        ReportedError.objects.select_related("reporter", "resolved_by"),
        pk=reported_error_id,
    )
    if not event.is_resolved:
        event.is_resolved = True
        event.resolved_at = timezone.now()
        event.resolved_by = request.user
        event.save(update_fields=["is_resolved", "resolved_at", "resolved_by"])
        record_audit_event(
            action="error.report.resolved",
            actor=request.user,
            target=event,
            summary=f"Resolved reported error: {event.title}",
            metadata={"reporter_email": event.reporter.email if event.reporter else ""},
            request=request,
        )

    return JsonResponse({"reported_error": serialize_reported_error(event)})
