from django.db.models import Count, Q

from recognition.services import build_points_table

from .models import BrandStoreItem, BrandStoreRedemption
from .serializers import serialize_redemption, serialize_store_item


ACTIVE_REDEMPTION_STATUSES = {
    BrandStoreRedemption.Status.REQUESTED,
    BrandStoreRedemption.Status.APPROVED,
    BrandStoreRedemption.Status.FULFILLED,
}


def earned_points_for_user(user):
    if not getattr(user, "is_authenticated", False):
        return 0
    match = next((row for row in build_points_table() if row["user_id"] == user.id), None)
    return match["points"] if match else 0


def locked_points_for_user(user):
    if not getattr(user, "is_authenticated", False):
        return 0
    return sum(
        user.brand_store_redemptions.filter(status__in=ACTIVE_REDEMPTION_STATUSES)
        .values_list("points_locked", flat=True)
    )


def build_store_overview(user):
    active_counts = {
        row["id"]: row["active_redemptions"]
        for row in BrandStoreItem.objects.filter(is_active=True)
        .annotate(
            active_redemptions=Count(
                "redemptions",
                filter=Q(redemptions__status__in=ACTIVE_REDEMPTION_STATUSES),
            )
        )
        .values("id", "active_redemptions")
    }
    items = [
        serialize_store_item(item, active_redemptions=active_counts.get(item.id, 0))
        for item in BrandStoreItem.objects.filter(is_active=True).order_by("category", "point_cost", "name")
    ]
    redemptions = (
        BrandStoreRedemption.objects.select_related("item", "requester")
        .filter(requester=user)
        .order_by("-created_at")
        if getattr(user, "is_authenticated", False)
        else BrandStoreRedemption.objects.none()
    )
    earned = earned_points_for_user(user)
    locked = locked_points_for_user(user)

    return {
        "items": items,
        "my_redemptions": [serialize_redemption(redemption) for redemption in redemptions[:8]],
        "balance": {
            "earned_points": earned,
            "locked_points": locked,
            "available_points": max(earned - locked, 0),
        },
    }
