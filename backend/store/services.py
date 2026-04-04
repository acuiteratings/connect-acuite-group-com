from collections import Counter, defaultdict

from django.db.models import Count, Q
from django.utils import timezone

from feed.models import Comment, Post, PostReaction
from learning.models import BookRequisition

from .models import BrandStoreItem, BrandStoreRedemption, CoinLedgerEntry
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
    "ceo_request": {"label": "Connect with MD & CEO", "coins": 1000},
}


def build_coin_rules():
    return [
        {"key": key, "label": item["label"], "coins": item["coins"]}
        for key, item in COIN_RULES.items()
    ]


def default_coin_balance(*, include_register=False):
    payload = {
        "earned_points": 0,
        "locked_points": 0,
        "spent_points": 0,
        "available_points": 0,
    }
    if include_register:
        payload["register"] = []
    return payload


def _single_entry_reference(source_type, source_id, event_key, entry_type):
    return f"{source_type}:{source_id}:{event_key}:{entry_type}"


def _reward_cycle_prefix(source_type, source_id, event_key):
    return f"{source_type}:{source_id}:{event_key}:"


def _reward_cycle_reference(source_type, source_id, event_key, entry_type, cycle):
    return f"{source_type}:{source_id}:{event_key}:{entry_type}:{cycle}"


def _ensure_ledger_entry(
    *,
    user,
    entry_type,
    event_key,
    amount,
    reference_key,
    occurred_at,
    summary,
    metadata=None,
):
    if not getattr(user, "is_authenticated", False):
        return None, False
    entry, created = CoinLedgerEntry.objects.get_or_create(
        reference_key=reference_key,
        defaults={
            "user": user,
            "entry_type": entry_type,
            "event_key": event_key,
            "amount": amount,
            "occurred_at": occurred_at or timezone.now(),
            "summary": summary,
            "metadata": metadata or {},
        },
    )
    return entry, created


def _reward_cycle_counts(source_type, source_id, event_key):
    prefix = _reward_cycle_prefix(source_type, source_id, event_key)
    counts = Counter(
        CoinLedgerEntry.objects.filter(
            reference_key__startswith=prefix,
            entry_type__in=(
                CoinLedgerEntry.EntryType.EARN,
                CoinLedgerEntry.EntryType.EARN_REVERSAL,
            ),
        ).values_list("entry_type", flat=True)
    )
    return (
        counts[CoinLedgerEntry.EntryType.EARN],
        counts[CoinLedgerEntry.EntryType.EARN_REVERSAL],
    )


def _ensure_reward_entry(
    *,
    qualifies,
    user,
    source_type,
    source_id,
    event_key,
    occurred_at,
    summary,
    metadata=None,
):
    if not getattr(user, "is_authenticated", False) or not source_id:
        return None, False

    earn_count, reversal_count = _reward_cycle_counts(source_type, source_id, event_key)
    amount = COIN_RULES[event_key]["coins"]

    if qualifies:
        if earn_count > reversal_count:
            return None, False
        cycle = earn_count + 1
        return _ensure_ledger_entry(
            user=user,
            entry_type=CoinLedgerEntry.EntryType.EARN,
            event_key=event_key,
            amount=amount,
            reference_key=_reward_cycle_reference(
                source_type,
                source_id,
                event_key,
                CoinLedgerEntry.EntryType.EARN,
                cycle,
            ),
            occurred_at=occurred_at,
            summary=summary,
            metadata=metadata,
        )

    if earn_count <= reversal_count:
        return None, False

    cycle = reversal_count + 1
    return _ensure_ledger_entry(
        user=user,
        entry_type=CoinLedgerEntry.EntryType.EARN_REVERSAL,
        event_key=event_key,
        amount=amount,
        reference_key=_reward_cycle_reference(
            source_type,
            source_id,
            event_key,
            CoinLedgerEntry.EntryType.EARN_REVERSAL,
            cycle,
        ),
        occurred_at=occurred_at or timezone.now(),
        summary=f"Reversed: {summary}",
        metadata=metadata,
    )


def sync_coin_ledger_for_reaction(reaction):
    if reaction.reaction_type != PostReaction.ReactionType.LIKE:
        return None, False
    return _ensure_reward_entry(
        qualifies=True,
        user=reaction.user,
        source_type="reaction",
        source_id=reaction.id,
        event_key="reaction_given",
        occurred_at=reaction.created_at,
        summary=f"Liked '{reaction.post.title}'",
        metadata={"post_id": reaction.post_id, "reaction_type": reaction.reaction_type},
    )


def reverse_coin_ledger_for_reaction(reaction):
    if reaction.reaction_type != PostReaction.ReactionType.LIKE:
        return None, False
    return _ensure_reward_entry(
        qualifies=False,
        user=reaction.user,
        source_type="reaction",
        source_id=reaction.id,
        event_key="reaction_given",
        occurred_at=timezone.now(),
        summary=f"Liked '{reaction.post.title}'",
        metadata={"post_id": reaction.post_id, "reaction_type": reaction.reaction_type},
    )


def sync_coin_ledger_for_comment(comment):
    return _ensure_reward_entry(
        qualifies=comment.moderation_status == Comment.ModerationStatus.PUBLISHED,
        user=comment.author,
        source_type="comment",
        source_id=comment.id,
        event_key="published_comment",
        occurred_at=comment.created_at,
        summary=f"Commented on '{comment.post.title}'",
        metadata={"post_id": comment.post_id},
    )


def reverse_coin_ledger_for_comment(comment):
    return _ensure_reward_entry(
        qualifies=False,
        user=comment.author,
        source_type="comment",
        source_id=comment.id,
        event_key="published_comment",
        occurred_at=timezone.now(),
        summary=f"Commented on '{comment.post.title}'",
        metadata={"post_id": comment.post_id},
    )


def _post_reward_key(post):
    if post.module != Post.Module.EMPLOYEE_POSTS:
        return ""
    metadata = post.metadata or {}
    if metadata.get("town_hall_response"):
        return "question_asked"
    if metadata.get("ceo_desk_request"):
        return "ceo_request"
    if metadata.get("submission_key") == "share_idea":
        return "idea_shared"
    return ""


def sync_coin_ledger_for_post(post):
    reward_key = _post_reward_key(post)
    if not reward_key:
        return None, False
    return _ensure_reward_entry(
        qualifies=post.moderation_status == Post.ModerationStatus.PUBLISHED,
        user=post.author,
        source_type="post",
        source_id=post.id,
        event_key=reward_key,
        occurred_at=post.published_at or post.created_at or timezone.now(),
        summary=f"Approved '{post.title}'",
        metadata={
            "post_id": post.id,
            "submission_key": (post.metadata or {}).get("submission_key", ""),
        },
    )


def sync_coin_ledger_for_book_requisition(requisition):
    return _ensure_reward_entry(
        qualifies=(
            requisition.status == BookRequisition.Status.RETURNED
            and requisition.returned_at is not None
        ),
        user=requisition.requester,
        source_type="book_requisition",
        source_id=requisition.id,
        event_key="book_returned",
        occurred_at=requisition.returned_at or requisition.updated_at or timezone.now(),
        summary=f"Returned '{requisition.book.title}'",
        metadata={"book_id": requisition.book_id},
    )


def sync_coin_ledger_for_redemption(redemption):
    if not redemption.requester_id:
        return None, False

    hold_reference = _single_entry_reference(
        "redemption",
        redemption.id,
        "store_request",
        CoinLedgerEntry.EntryType.HOLD,
    )
    release_reference = _single_entry_reference(
        "redemption",
        redemption.id,
        "store_request",
        CoinLedgerEntry.EntryType.RELEASE,
    )
    spend_reference = _single_entry_reference(
        "redemption",
        redemption.id,
        "store_request",
        CoinLedgerEntry.EntryType.SPEND,
    )
    metadata = {"item_id": redemption.item_id, "redemption_id": redemption.id}

    _ensure_ledger_entry(
        user=redemption.requester,
        entry_type=CoinLedgerEntry.EntryType.HOLD,
        event_key="store_request",
        amount=redemption.points_locked,
        reference_key=hold_reference,
        occurred_at=redemption.created_at or timezone.now(),
        summary=f"Requested {redemption.item.name}",
        metadata=metadata,
    )

    if redemption.status in {
        BrandStoreRedemption.Status.CANCELLED,
        BrandStoreRedemption.Status.DECLINED,
        BrandStoreRedemption.Status.APPROVED,
        BrandStoreRedemption.Status.FULFILLED,
    }:
        _ensure_ledger_entry(
            user=redemption.requester,
            entry_type=CoinLedgerEntry.EntryType.RELEASE,
            event_key="store_request",
            amount=redemption.points_locked,
            reference_key=release_reference,
            occurred_at=redemption.reviewed_at or redemption.updated_at or timezone.now(),
            summary=f"Released hold for {redemption.item.name}",
            metadata=metadata,
        )

    if redemption.status in SPENT_REDEMPTION_STATUSES:
        _ensure_ledger_entry(
            user=redemption.requester,
            entry_type=CoinLedgerEntry.EntryType.SPEND,
            event_key="store_request",
            amount=redemption.points_locked,
            reference_key=spend_reference,
            occurred_at=redemption.reviewed_at or redemption.updated_at or timezone.now(),
            summary=f"Collected {redemption.item.name}",
            metadata=metadata,
        )
    return None, False


def _signed_register_amount(entry):
    if entry.entry_type in {
        CoinLedgerEntry.EntryType.EARN,
        CoinLedgerEntry.EntryType.RELEASE,
    }:
        return entry.amount
    return -entry.amount


def _register_kind(entry):
    if entry.entry_type == CoinLedgerEntry.EntryType.HOLD:
        return "locked"
    if entry.entry_type == CoinLedgerEntry.EntryType.RELEASE:
        return "released"
    if entry.entry_type == CoinLedgerEntry.EntryType.SPEND:
        return "spent"
    if entry.entry_type == CoinLedgerEntry.EntryType.EARN_REVERSAL:
        return "reversed"
    return "earned"


def build_coin_balance_map(user_ids, *, include_register=False, register_limit=12):
    user_ids = [int(user_id) for user_id in user_ids if user_id]
    if not user_ids:
        return {}

    payload = {
        user_id: {
            "earned_total": 0,
            "earned_reversals": 0,
            "held_total": 0,
            "released_total": 0,
            "spent_points": 0,
            "register": [] if include_register else None,
        }
        for user_id in user_ids
    }

    entries = CoinLedgerEntry.objects.filter(user_id__in=user_ids).order_by("-occurred_at", "-id")

    for entry in entries:
        balance = payload[entry.user_id]
        if entry.entry_type == CoinLedgerEntry.EntryType.EARN:
            balance["earned_total"] += entry.amount
        elif entry.entry_type == CoinLedgerEntry.EntryType.EARN_REVERSAL:
            balance["earned_reversals"] += entry.amount
        elif entry.entry_type == CoinLedgerEntry.EntryType.HOLD:
            balance["held_total"] += entry.amount
        elif entry.entry_type == CoinLedgerEntry.EntryType.RELEASE:
            balance["released_total"] += entry.amount
        elif entry.entry_type == CoinLedgerEntry.EntryType.SPEND:
            balance["spent_points"] += entry.amount

        if include_register and len(balance["register"]) < register_limit:
            balance["register"].append(
                {
                    "occurred_at": entry.occurred_at.isoformat() if entry.occurred_at else None,
                    "amount": _signed_register_amount(entry),
                    "label": COIN_RULES.get(entry.event_key, {}).get("label") or entry.get_entry_type_display(),
                    "summary": entry.summary,
                    "kind": _register_kind(entry),
                }
            )

    final_payload = {}
    for user_id, raw_balance in payload.items():
        earned_points = max(raw_balance["earned_total"] - raw_balance["earned_reversals"], 0)
        locked_points = max(raw_balance["held_total"] - raw_balance["released_total"], 0)
        spent_points = raw_balance["spent_points"]
        balance = {
            "earned_points": earned_points,
            "locked_points": locked_points,
            "spent_points": spent_points,
            "available_points": max(earned_points - spent_points, 0),
        }
        if include_register:
            balance["register"] = raw_balance["register"]
        final_payload[user_id] = balance
    return final_payload


def coin_balance_for_user(user, *, include_register=False):
    if not getattr(user, "is_authenticated", False):
        return default_coin_balance(include_register=include_register)
    return build_coin_balance_map([user.id], include_register=include_register).get(
        user.id,
        default_coin_balance(include_register=include_register),
    )


def earned_points_for_user(user):
    return coin_balance_for_user(user)["earned_points"]


def locked_points_for_user(user):
    return coin_balance_for_user(user)["locked_points"]


def spent_points_for_user(user):
    return coin_balance_for_user(user)["spent_points"]


def pending_requested_points_for_user(user):
    return locked_points_for_user(user)


def requestable_points_for_user(user):
    balance = coin_balance_for_user(user)
    return max(balance["earned_points"] - balance["spent_points"] - balance["locked_points"], 0)


def backfill_coin_ledger():
    for reaction in PostReaction.objects.filter(
        reaction_type=PostReaction.ReactionType.LIKE,
    ).select_related("post", "user"):
        sync_coin_ledger_for_reaction(reaction)

    for comment in Comment.objects.select_related("post", "author"):
        sync_coin_ledger_for_comment(comment)

    for post in Post.objects.select_related("author"):
        sync_coin_ledger_for_post(post)

    for requisition in BookRequisition.objects.select_related("book", "requester"):
        sync_coin_ledger_for_book_requisition(requisition)

    for redemption in BrandStoreRedemption.objects.select_related("item", "requester"):
        sync_coin_ledger_for_redemption(redemption)


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
    balance = coin_balance_for_user(user, include_register=True)

    return {
        "items": items,
        "my_redemptions": [serialize_redemption(redemption) for redemption in redemptions[:8]],
        "balance": balance,
        "coin_rules": build_coin_rules(),
    }
