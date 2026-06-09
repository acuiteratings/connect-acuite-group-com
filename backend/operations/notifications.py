import json
from datetime import timedelta

from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import OrgNotification, OrgNotificationRead
from .serializers import serialize_org_notification


ORG_NOTIFICATION_RETENTION_DAYS = 60


def _parse_json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return {}


def _authenticated_employee_required(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)
    if not getattr(request.user, "has_employee_access", False):
        return JsonResponse({"detail": "Employee access required."}, status=403)
    return None


def create_org_notification(*, title, message="", category=OrgNotification.Category.GENERAL, target_tab="", target_url="", metadata=None, actor=None):
    clean_title = str(title or "").strip()
    if not clean_title:
        return None
    return OrgNotification.objects.create(
        title=clean_title[:180],
        message=str(message or "").strip(),
        category=category if category in OrgNotification.Category.values else OrgNotification.Category.GENERAL,
        target_tab=str(target_tab or "").strip()[:64],
        target_url=str(target_url or "").strip()[:255],
        metadata=metadata if isinstance(metadata, dict) else {},
        created_by=actor if getattr(actor, "is_authenticated", False) else None,
    )


def notifications_collection(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    access_error = _authenticated_employee_required(request)
    if access_error:
        return access_error

    cutoff = timezone.now() - timedelta(days=ORG_NOTIFICATION_RETENTION_DAYS)
    queryset = OrgNotification.objects.select_related("created_by").filter(
        is_active=True,
        created_at__gte=cutoff,
    )
    read_ids = set(
        OrgNotificationRead.objects.filter(
            user=request.user,
            notification__in=queryset,
        ).values_list("notification_id", flat=True)
    )
    unread_count = queryset.exclude(reads__user=request.user).count()
    try:
        limit = int(request.GET.get("limit", 20))
    except (TypeError, ValueError):
        limit = 20
    limit = min(max(limit, 1), 50)
    results = [
        serialize_org_notification(notification, read_ids=read_ids)
        for notification in queryset[:limit]
    ]
    return JsonResponse(
        {
            "count": len(results),
            "unread_count": unread_count,
            "results": results,
        }
    )


def notification_mark_read(request, notification_id):
    if request.method != "PATCH":
        return HttpResponseNotAllowed(["PATCH"])
    access_error = _authenticated_employee_required(request)
    if access_error:
        return access_error

    notification = get_object_or_404(
        OrgNotification.objects.filter(is_active=True),
        pk=notification_id,
    )
    OrgNotificationRead.objects.get_or_create(notification=notification, user=request.user)
    return JsonResponse(
        {
            "notification": serialize_org_notification(notification, read_ids={notification.id}),
        }
    )


def notifications_mark_all_read(request):
    if request.method != "PATCH":
        return HttpResponseNotAllowed(["PATCH"])
    access_error = _authenticated_employee_required(request)
    if access_error:
        return access_error

    payload = _parse_json_body(request)
    ids = payload.get("ids")
    cutoff = timezone.now() - timedelta(days=ORG_NOTIFICATION_RETENTION_DAYS)
    queryset = OrgNotification.objects.filter(is_active=True, created_at__gte=cutoff)
    if isinstance(ids, list) and ids:
        queryset = queryset.filter(id__in=[int(item) for item in ids if str(item).isdigit()])
    existing_ids = set(
        OrgNotificationRead.objects.filter(
            user=request.user,
            notification__in=queryset,
        ).values_list("notification_id", flat=True)
    )
    reads = [
        OrgNotificationRead(notification=notification, user=request.user)
        for notification in queryset
        if notification.id not in existing_ids
    ]
    if reads:
        OrgNotificationRead.objects.bulk_create(reads, ignore_conflicts=True)
    unread_count = queryset.exclude(reads__user=request.user).count()
    return JsonResponse({"marked_read": len(reads), "unread_count": unread_count})
