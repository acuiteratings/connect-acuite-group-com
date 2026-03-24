import json

from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from operations.services import record_analytics_event, record_audit_event

from .models import BrandStoreItem, BrandStoreRedemption
from .serializers import serialize_redemption
from .services import ACTIVE_REDEMPTION_STATUSES, build_store_overview, locked_points_for_user, earned_points_for_user


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


@csrf_exempt
def redemption_collection(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
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

    earned = earned_points_for_user(request.user)
    locked = locked_points_for_user(request.user)
    available = max(earned - locked, 0)
    if available < item.point_cost:
        return JsonResponse({"detail": "Not enough available points for this redemption."}, status=400)

    redemption = BrandStoreRedemption.objects.create(
        item=item,
        requester=request.user,
        points_locked=item.point_cost,
        notes=str(payload.get("notes", "")).strip(),
    )
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
