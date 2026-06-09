import json

from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from accounts.models import User

from .models import ReportedError
from .serializers import serialize_reported_error
from .services import record_audit_event


def _parse_json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return {}


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
    payload = _parse_json_body(request)
    outcome = str(payload.get("resolution_outcome") or "resolved").strip()
    if outcome not in {ReportedError.ResolutionOutcome.RESOLVED, ReportedError.ResolutionOutcome.NOT_AN_ERROR}:
        return JsonResponse({"detail": "Choose Resolved or Not an error."}, status=400)
    resolution_comment = str(payload.get("resolution_comment") or "").strip()
    attachment_deleted = bool(event.attachment_data_url)
    if not event.is_resolved:
        event.is_resolved = True
        event.resolved_at = timezone.now()
        event.resolved_by = request.user
    event.resolution_outcome = outcome
    event.resolution_comment = resolution_comment
    event.reporter_seen_at = None
    event.attachment_name = ""
    event.attachment_content_type = ""
    event.attachment_size = 0
    event.attachment_data_url = ""
    event.save(
        update_fields=[
            "is_resolved",
            "resolved_at",
            "resolved_by",
            "resolution_outcome",
            "resolution_comment",
            "reporter_seen_at",
            "attachment_name",
            "attachment_content_type",
            "attachment_size",
            "attachment_data_url",
        ]
    )
    record_audit_event(
        action="error.report.resolved",
        actor=request.user,
        target=event,
        summary=f"Closed reported error as {event.get_resolution_outcome_display()}: {event.title}",
        metadata={
            "reporter_email": event.reporter.email if event.reporter else "",
            "resolution_outcome": event.resolution_outcome,
            "comment_present": bool(event.resolution_comment),
            "attachment_deleted": attachment_deleted,
        },
        request=request,
    )

    return JsonResponse({"reported_error": serialize_reported_error(event)})


def reported_error_notifications(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)

    queryset = ReportedError.objects.select_related("reporter", "resolved_by").filter(
        reporter=request.user,
        is_resolved=True,
        reporter_seen_at__isnull=True,
    )
    results = [serialize_reported_error(event) for event in queryset[:5]]
    return JsonResponse({"count": len(results), "results": results})


def reported_error_notification_acknowledge(request, reported_error_id):
    if request.method != "PATCH":
        return HttpResponseNotAllowed(["PATCH"])
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)

    event = get_object_or_404(
        ReportedError.objects.select_related("reporter", "resolved_by"),
        pk=reported_error_id,
        reporter=request.user,
    )
    if not event.reporter_seen_at:
        event.reporter_seen_at = timezone.now()
        event.save(update_fields=["reporter_seen_at"])
    return JsonResponse({"reported_error": serialize_reported_error(event)})
