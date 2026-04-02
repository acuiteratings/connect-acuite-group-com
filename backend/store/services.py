from collections import defaultdict

from django.db.models import Count, Q

from feed.models import Comment, Post, PostReaction
from learning.models import BookRequisition
from .models import BrandStoreItem, BrandStoreRedemption
from .serializers import serialize_redemption, serialize_store_item


ACTIVE_REDEMPTION_STATUSES = {
    BrandStoreRedemption.Status.REQUESTED,
    BrandStoreRedemption.Status.APPROVED,
    BrandStoreRedemption.Status.FULFILLED,
}
LOCKED_REDEMPTION_STATUSES = {
    BrandStoreRedemption.Status.REQUESTED,
}
SPENT_REDEMPTION_STATUSES = {
    BrandStoreRedemption.Status.APPROVED,
    BrandStoreRedemption.Status.FULFILLED,
}

COIN_RULES = {
    "reaction_given": {"label": "Like a post", "coins": 1},
    "published_comment": {"label": "Post a comment", "coins": 10},
    "book_returned": {"label": "Read and return a library book", "coins": 100},
    "idea_shared": {"label": "Share an idea", "coins": 500},
    "question_asked": {"label": "Ask a question", "coins": 1000},
}


def build_coin_rules():
    return [
        {"key": key, "label": item["label"], "coins": item["coins"]}
        for key, item in COIN_RULES.items()
    ]


def earned_points_for_user(user):
    if not getattr(user, "is_authenticated", False):
        return 0
    return build_coin_balance_map([user.id]).get(user.id, default_coin_balance())["earned_points"]


def locked_points_for_user(user):
    if not getattr(user, "is_authenticated", False):
        return 0
    return sum(
        user.brand_store_redemptions.filter(status__in=LOCKED_REDEMPTION_STATUSES)
        .values_list("points_locked", flat=True)
    )


def spent_points_for_user(user):
    if not getattr(user, "is_authenticated", False):
        return 0
    return sum(
        user.brand_store_redemptions.filter(status__in=SPENT_REDEMPTION_STATUSES)
        .values_list("points_locked", flat=True)
    )


def default_coin_balance():
    return {
        "earned_points": 0,
        "locked_points": 0,
        "spent_points": 0,
        "available_points": 0,
    }


def _append_entry(entries_by_user, user_id, *, occurred_at, amount, label, summary, kind):
    if user_id not in entries_by_user:
        return
    entries_by_user[user_id].append(
        {
            "occurred_at": occurred_at,
            "amount": amount,
            "label": label,
            "summary": summary,
            "kind": kind,
        }
    )


def build_coin_balance_map(user_ids, *, include_register=False, register_limit=12):
    user_ids = [int(user_id) for user_id in user_ids if user_id]
    if not user_ids:
        return {}

    earned = defaultdict(int)
    locked = defaultdict(int)
    spent = defaultdict(int)
    entries_by_user = {user_id: [] for user_id in user_ids} if include_register else {}

    for row in (
        PostReaction.objects.filter(
            user_id__in=user_ids,
            reaction_type=PostReaction.ReactionType.LIKE,
        )
        .values("user_id")
        .order_by()
        .annotate(count=Count("id"))
    ):
        user_id = row["user_id"]
        amount = row["count"] * COIN_RULES["reaction_given"]["coins"]
        earned[user_id] += amount
    if include_register:
        for reaction in PostReaction.objects.filter(
            user_id__in=user_ids,
            reaction_type=PostReaction.ReactionType.LIKE,
        ).select_related("post", "user"):
            _append_entry(
                entries_by_user,
                reaction.user_id,
                occurred_at=reaction.created_at,
                amount=COIN_RULES["reaction_given"]["coins"],
                label=COIN_RULES["reaction_given"]["label"],
                summary=f"Liked '{reaction.post.title}'",
                kind="earned",
            )

    for row in (
        Comment.objects.filter(
            author_id__in=user_ids,
            moderation_status=Comment.ModerationStatus.PUBLISHED,
        )
        .values("author_id")
        .order_by()
        .annotate(count=Count("id"))
    ):
        user_id = row["author_id"]
        amount = row["count"] * COIN_RULES["published_comment"]["coins"]
        earned[user_id] += amount
    if include_register:
        for comment in Comment.objects.filter(
            author_id__in=user_ids,
            moderation_status=Comment.ModerationStatus.PUBLISHED,
        ).select_related("post", "author"):
            _append_entry(
                entries_by_user,
                comment.author_id,
                occurred_at=comment.created_at,
                amount=COIN_RULES["published_comment"]["coins"],
                label=COIN_RULES["published_comment"]["label"],
                summary=f"Commented on '{comment.post.title}'",
                kind="earned",
            )

    for row in (
        Post.objects.filter(
            author_id__in=user_ids,
            module=Post.Module.IDEAS_VOICE,
            topic="idea",
            moderation_status=Post.ModerationStatus.PUBLISHED,
        )
        .values("author_id")
        .order_by()
        .annotate(count=Count("id"))
    ):
        user_id = row["author_id"]
        amount = row["count"] * COIN_RULES["idea_shared"]["coins"]
        earned[user_id] += amount
    if include_register:
        for post in Post.objects.filter(
            author_id__in=user_ids,
            module=Post.Module.IDEAS_VOICE,
            topic="idea",
            moderation_status=Post.ModerationStatus.PUBLISHED,
        ).select_related("author"):
            _append_entry(
                entries_by_user,
                post.author_id,
                occurred_at=post.published_at or post.created_at,
                amount=COIN_RULES["idea_shared"]["coins"],
                label=COIN_RULES["idea_shared"]["label"],
                summary=f"Shared '{post.title}'",
                kind="earned",
            )

    for row in (
        BookRequisition.objects.filter(
            requester_id__in=user_ids,
            status=BookRequisition.Status.RETURNED,
            returned_at__isnull=False,
        )
        .values("requester_id")
        .order_by()
        .annotate(count=Count("id"))
    ):
        user_id = row["requester_id"]
        amount = row["count"] * COIN_RULES["book_returned"]["coins"]
        earned[user_id] += amount
    if include_register:
        for requisition in BookRequisition.objects.filter(
            requester_id__in=user_ids,
            status=BookRequisition.Status.RETURNED,
            returned_at__isnull=False,
        ).select_related("book", "requester"):
            _append_entry(
                entries_by_user,
                requisition.requester_id,
                occurred_at=requisition.returned_at,
                amount=COIN_RULES["book_returned"]["coins"],
                label=COIN_RULES["book_returned"]["label"],
                summary=f"Returned '{requisition.book.title}'",
                kind="earned",
            )

    for redemption in BrandStoreRedemption.objects.filter(
        requester_id__in=user_ids,
        status__in=LOCKED_REDEMPTION_STATUSES,
    ).select_related("item", "requester"):
        locked[redemption.requester_id] += redemption.points_locked
        if include_register:
            _append_entry(
                entries_by_user,
                redemption.requester_id,
                occurred_at=redemption.created_at,
                amount=-redemption.points_locked,
                label="Purchase request pending",
                summary=f"Requested {redemption.item.name}",
                kind="locked",
            )

    for redemption in BrandStoreRedemption.objects.filter(
        requester_id__in=user_ids,
        status__in=SPENT_REDEMPTION_STATUSES,
    ).select_related("item", "requester"):
        spent[redemption.requester_id] += redemption.points_locked
        if include_register:
            _append_entry(
                entries_by_user,
                redemption.requester_id,
                occurred_at=redemption.reviewed_at or redemption.updated_at,
                amount=-redemption.points_locked,
                label="Acuite Coins encashed",
                summary=f"Collected {redemption.item.name}",
                kind="spent",
            )

    payload = {}
    for user_id in user_ids:
        balance = {
            "earned_points": earned[user_id],
            "locked_points": locked[user_id],
            "spent_points": spent[user_id],
            "available_points": max(earned[user_id] - locked[user_id] - spent[user_id], 0),
        }
        if include_register:
            entries = sorted(
                entries_by_user[user_id],
                key=lambda item: item["occurred_at"] or 0,
                reverse=True,
            )[:register_limit]
            balance["register"] = [
                {
                    **item,
                    "occurred_at": item["occurred_at"].isoformat() if item["occurred_at"] else None,
                }
                for item in entries
            ]
        payload[user_id] = balance
    return payload


def build_store_admin_overview():
    redemptions = BrandStoreRedemption.objects.select_related("item", "requester").order_by("-created_at")
    return {
        "requests": [
            serialize_redemption(item)
            for item in redemptions.filter(status=BrandStoreRedemption.Status.REQUESTED)[:100]
        ],
        "handed_over": [
            serialize_redemption(item)
            for item in redemptions.filter(status__in=SPENT_REDEMPTION_STATUSES)[:100]
        ],
    }


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
    balance = build_coin_balance_map([user.id], include_register=True).get(user.id, default_coin_balance()) if getattr(user, "is_authenticated", False) else default_coin_balance()

    return {
        "items": items,
        "my_redemptions": [serialize_redemption(redemption) for redemption in redemptions[:8]],
        "balance": balance,
        "coin_rules": build_coin_rules(),
    }
