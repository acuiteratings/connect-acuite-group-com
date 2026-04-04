import json

from django.db import IntegrityError
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from operations.services import record_analytics_event, record_audit_event

from .models import BrandStoreItem, BrandStoreRedemption
from .serializers import serialize_redemption
from .services import (
    ACTIVE_REDEMPTION_STATUSES,
    build_store_admin_overview,
    build_store_overview,
    coin_balance_for_user,
    requestable_points_for_user,
)


def _parse_json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Request body must be valid JSON.") from exc


def store_overview(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    return JsonResponse(build_store_overview(request.user))


def store_admin_overview(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    if not request.user.is_authenticated or not request.user.can_administer_connect:
        return JsonResponse({"detail": "Admin access required."}, status=403)
    return JsonResponse(build_store_admin_overview())


def redemption_collection(request):
    if request.method == "GET":
        if not request.user.is_authenticated or not request.user.can_administer_connect:
            return JsonResponse({"detail": "Admin access required."}, status=403)
        return JsonResponse(build_store_admin_overview())
    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)

    try:
        payload = _parse_json_body(request)
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    item_id = payload.get("item_id")
    if not item_id:
        return JsonResponse({"detail": "item_id is required."}, status=400)

    item = get_object_or_404(BrandStoreItem, pk=item_id, is_active=True)
    active_redemptions = item.redemptions.filter(status__in=ACTIVE_REDEMPTION_STATUSES).count()
    if active_redemptions >= item.stock_units:
        return JsonResponse({"detail": "This item is currently out of stock."}, status=400)

    if requestable_points_for_user(request.user) < item.point_cost:
        return JsonResponse({"detail": "Not enough Acuite Coins available for this request."}, status=400)

    try:
        redemption = BrandStoreRedemption.objects.create(
            item=item,
            requester=request.user,
            points_locked=item.point_cost,
            notes=str(payload.get("notes", "")).strip(),
        )
    except IntegrityError:
        return JsonResponse({"detail": "You already have an open request for this item."}, status=400)
    record_audit_event(
        action="store.redemption_requested",
        actor=request.user,
        target=redemption,
        summary=f"Requested store item '{item.name}'",
        metadata={"item_id": item.id, "points_locked": item.point_cost},
        request=request,
    )
    record_analytics_event(
        "store",
        "redemption_requested",
        actor=request.user,
        metadata={"item_id": item.id, "points_locked": item.point_cost},
        request=request,
    )
    return JsonResponse({"redemption": serialize_redemption(redemption)}, status=201)


def redemption_detail(request, redemption_id):
    if request.method not in {"GET", "PATCH"}:
        return HttpResponseNotAllowed(["GET", "PATCH"])
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)

    redemption = get_object_or_404(
        BrandStoreRedemption.objects.select_related("item", "requester"),
        pk=redemption_id,
    )

    if request.method == "GET":
        if request.user.can_administer_connect or redemption.requester_id == request.user.id:
            return JsonResponse({"redemption": serialize_redemption(redemption)})
        return JsonResponse({"detail": "You cannot view this redemption."}, status=403)

    try:
        payload = _parse_json_body(request)
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    status = str(payload.get("status", "")).strip().lower()
    admin_note = str(payload.get("admin_note", "")).strip()

    if request.user.can_administer_connect:
        if status not in {
            BrandStoreRedemption.Status.APPROVED,
            BrandStoreRedemption.Status.DECLINED,
            BrandStoreRedemption.Status.FULFILLED,
        }:
            return JsonResponse({"detail": "Unsupported redemption status."}, status=400)
        current_status = redemption.status
        allowed_admin_transitions = {
            BrandStoreRedemption.Status.REQUESTED: {
                BrandStoreRedemption.Status.APPROVED,
                BrandStoreRedemption.Status.DECLINED,
            },
            BrandStoreRedemption.Status.APPROVED: {
                BrandStoreRedemption.Status.FULFILLED,
            },
            BrandStoreRedemption.Status.FULFILLED: set(),
            BrandStoreRedemption.Status.DECLINED: set(),
            BrandStoreRedemption.Status.CANCELLED: set(),
        }
        if status not in allowed_admin_transitions.get(current_status, set()):
            return JsonResponse(
                {"detail": "This redemption cannot move to that status from its current state."},
                status=400,
            )
        if status == BrandStoreRedemption.Status.APPROVED:
            balance = coin_balance_for_user(redemption.requester)
            available = max(balance["earned_points"] - balance["spent_points"], 0)
            if available < redemption.points_locked:
                return JsonResponse({"detail": "This employee no longer has enough Acuite Coins for approval."}, status=400)
        redemption.status = status
        redemption.admin_note = admin_note
        redemption.reviewed_at = timezone.now()
        redemption.save(update_fields=["status", "admin_note", "reviewed_at", "updated_at"])
        record_audit_event(
            action=f"store.redemption_{status}",
            actor=request.user,
            target=redemption,
            summary=f"Marked store redemption for '{redemption.item.name}' as {status}",
            metadata={"redemption_id": redemption.id, "status": status},
            request=request,
        )
        record_analytics_event(
            "store",
            f"redemption_{status}",
            actor=request.user,
            metadata={"redemption_id": redemption.id, "item_id": redemption.item_id},
            request=request,
        )
        return JsonResponse({"redemption": serialize_redemption(redemption)})

    if redemption.requester_id != request.user.id:
        return JsonResponse({"detail": "You cannot update this redemption."}, status=403)
    if status != BrandStoreRedemption.Status.CANCELLED:
        return JsonResponse({"detail": "Only cancellation is allowed here."}, status=400)
    if redemption.status != BrandStoreRedemption.Status.REQUESTED:
        return JsonResponse({"detail": "This request can no longer be cancelled."}, status=400)

    redemption.status = BrandStoreRedemption.Status.CANCELLED
    redemption.save(update_fields=["status", "updated_at"])
    record_audit_event(
        action="store.redemption_cancelled",
        actor=request.user,
        target=redemption,
        summary=f"Cancelled store redemption for '{redemption.item.name}'",
        metadata={"redemption_id": redemption.id},
        request=request,
    )
    return JsonResponse({"redemption": serialize_redemption(redemption)})
