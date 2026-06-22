import hashlib
import json
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from feed.models import Post
from feed.serializers import serialize_post
from operations.models import OrgNotification
from operations.notifications import create_org_notification


ANNOUNCEMENT_TAG_LABELS = {
    "leadership": "Leadership",
    "people_culture": "People & Culture",
    "cybersecurity": "Cybersecurity",
    "compliance": "Compliance",
    "regulations": "Regulations",
    "new_initiatives": "New Initiatives",
    "giving": "Giving",
    "opinion_poll": "Opinion Poll",
}


def _announcement_content_signature(post):
    serialized = serialize_post(post)
    payload = {
        "title": serialized.get("title", ""),
        "body": serialized.get("body", ""),
        "bulletin_meta_lines": (serialized.get("metadata") or {}).get("bulletin_meta_lines", []),
        "home_announcement_display": (serialized.get("metadata") or {}).get("home_announcement_display", {}),
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, ensure_ascii=True).encode("utf-8")
    ).hexdigest()


def _announcement_has_runtime_override(post):
    serialized = serialize_post(post)
    return (
        serialized.get("title") != post.title
        or serialized.get("body") != post.body
        or (serialized.get("metadata") or {}) != (post.metadata or {})
    )


class Command(BaseCommand):
    help = "Backfill missing org notifications for recent or runtime-overridden home announcements."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            type=int,
            default=3,
            help="Look back this many days for saved announcement updates.",
        )

    def handle(self, *args, **options):
        now = timezone.now()
        lookback_days = max(int(options["days"] or 1), 1)
        cutoff = now - timedelta(days=lookback_days)
        created = 0
        examined = 0

        posts = (
            Post.objects.select_related("author")
            .filter(
                module=Post.Module.BULLETIN,
                topic="announcements",
                visibility=Post.Visibility.COMPANY,
                moderation_status=Post.ModerationStatus.PUBLISHED,
                metadata__has_key="home_announcement_tag",
            )
            .order_by("-updated_at", "-created_at")
        )

        for post in posts:
            metadata = dict(post.metadata or {})
            announcement_tag = str(metadata.get("home_announcement_tag", "")).strip().lower()
            if not announcement_tag:
                continue

            recent_saved_update = any(
                timestamp and timestamp >= cutoff
                for timestamp in (post.updated_at, post.published_at, post.created_at)
            )
            runtime_override_active = _announcement_has_runtime_override(post)
            if not recent_saved_update and not runtime_override_active:
                continue

            examined += 1
            signature = _announcement_content_signature(post)
            existing = OrgNotification.objects.filter(
                is_active=True,
                category=OrgNotification.Category.ANNOUNCEMENT,
                target_tab="home",
                metadata__home_announcement_filter=announcement_tag,
                metadata__content_signature=signature,
            ).exists()
            if existing:
                continue

            label = ANNOUNCEMENT_TAG_LABELS.get(
                announcement_tag,
                announcement_tag.replace("_", " ").title(),
            )
            serialized = serialize_post(post)
            notification = create_org_notification(
                title=f"{label} announcement updated",
                message=serialized.get("title", post.title),
                category=OrgNotification.Category.ANNOUNCEMENT,
                target_tab="home",
                metadata={
                    "post_id": post.id,
                    "source_post_id": post.id,
                    "home_announcement_filter": announcement_tag,
                    "content_signature": signature,
                    "source": "deploy_announcement_sync",
                },
                actor=post.author,
            )
            if notification:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Announcement notification sync complete: examined={examined}, created={created}"
            )
        )
