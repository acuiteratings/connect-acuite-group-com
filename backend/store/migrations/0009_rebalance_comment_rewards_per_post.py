from collections import Counter, defaultdict

from django.db import migrations
from django.db.models import Min
from django.utils import timezone


COMMENT_REWARD_COINS = 500
COMMENT_REWARD_EVENT_KEY = "published_comment"


def _reference_key(user_id, post_id, entry_type, cycle):
    return f"comment_post:{user_id}:{post_id}:{COMMENT_REWARD_EVENT_KEY}:{entry_type}:{cycle}"


def rebalance_comment_rewards_per_post(apps, schema_editor):
    Comment = apps.get_model("feed", "Comment")
    CoinLedgerEntry = apps.get_model("store", "CoinLedgerEntry")

    published_pairs = {}
    for row in (
        Comment.objects.filter(moderation_status="published")
        .values("author_id", "post_id")
        .annotate(first_created_at=Min("created_at"))
    ):
        published_pairs[(row["author_id"], row["post_id"])] = row["first_created_at"]

    reward_counts = defaultdict(Counter)
    for row in CoinLedgerEntry.objects.filter(event_key=COMMENT_REWARD_EVENT_KEY).values(
        "user_id",
        "metadata",
        "entry_type",
    ):
        metadata = row.get("metadata") or {}
        post_id = metadata.get("post_id")
        if not post_id:
            continue
        reward_counts[(row["user_id"], int(post_id))][row["entry_type"]] += 1

    all_pairs = set(published_pairs.keys()) | set(reward_counts.keys())
    now = timezone.now()

    for user_id, post_id in all_pairs:
        counts = reward_counts[(user_id, post_id)]
        earn_count = counts["earn"]
        reversal_count = counts["earn_reversal"]
        current_net = earn_count - reversal_count
        desired_net = 1 if (user_id, post_id) in published_pairs else 0

        if current_net == desired_net:
            continue

        if current_net < desired_net:
            for offset in range(desired_net - current_net):
                CoinLedgerEntry.objects.get_or_create(
                    reference_key=_reference_key(user_id, post_id, "earn", earn_count + offset + 1),
                    defaults={
                        "user_id": user_id,
                        "entry_type": "earn",
                        "event_key": COMMENT_REWARD_EVENT_KEY,
                        "amount": COMMENT_REWARD_COINS,
                        "occurred_at": published_pairs[(user_id, post_id)] or now,
                        "summary": "Commented on a post",
                        "metadata": {
                            "post_id": post_id,
                            "source": "comment_reward_rebalance",
                        },
                    },
                )
            continue

        for offset in range(current_net - desired_net):
            CoinLedgerEntry.objects.get_or_create(
                reference_key=_reference_key(user_id, post_id, "earn_reversal", reversal_count + offset + 1),
                defaults={
                    "user_id": user_id,
                    "entry_type": "earn_reversal",
                    "event_key": COMMENT_REWARD_EVENT_KEY,
                    "amount": COMMENT_REWARD_COINS,
                    "occurred_at": now,
                    "summary": "Reversed: Commented on a post",
                    "metadata": {
                        "post_id": post_id,
                        "source": "comment_reward_rebalance",
                    },
                },
            )


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0008_update_brand_store_catalog_june_2026"),
    ]

    operations = [
        migrations.RunPython(
            rebalance_comment_rewards_per_post,
            migrations.RunPython.noop,
        ),
    ]
