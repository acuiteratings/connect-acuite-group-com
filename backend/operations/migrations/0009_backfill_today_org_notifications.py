from datetime import datetime, time

from django.db import migrations
from django.db.models import Q
from django.utils import timezone


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


def _today_start():
    local_today = timezone.localdate()
    return timezone.make_aware(datetime.combine(local_today, time.min), timezone.get_current_timezone())


def _notification_exists_for_post(OrgNotification, post_id):
    return (
        OrgNotification.objects.filter(metadata__post_id=post_id).exists()
        or OrgNotification.objects.filter(metadata__source_post_id=post_id).exists()
    )


def _create_notification_for_post(OrgNotification, post):
    if _notification_exists_for_post(OrgNotification, post.id):
        return

    metadata = dict(post.metadata or {})
    notification_metadata = {
        "post_id": post.id,
        "source_post_id": post.id,
        "source": "today_backfill",
    }

    if metadata.get("event_post") or post.topic == "connect_events":
        notification_metadata.update(
            {
                "event_date": metadata.get("event_date", ""),
                "focus_sidebar": "events",
            }
        )
        OrgNotification.objects.create(
            title=f"Event update: {post.title}"[:180],
            message=(post.body or "")[:220],
            category="event",
            target_tab="home",
            metadata=notification_metadata,
            created_by_id=post.author_id,
        )
        return

    if not metadata.get("post_as_company"):
        return

    announcement_tag = str(metadata.get("home_announcement_tag", "")).strip().lower()
    if announcement_tag:
        label = ANNOUNCEMENT_TAG_LABELS.get(announcement_tag, announcement_tag.replace("_", " ").title())
        notification_metadata["home_announcement_filter"] = announcement_tag
        OrgNotification.objects.create(
            title=f"{label} announcement updated"[:180],
            message=post.title,
            category="announcement",
            target_tab="home",
            metadata=notification_metadata,
            created_by_id=post.author_id,
        )
        return

    bulletin_channel = str(metadata.get("bulletin_channel", "")).strip().lower()
    if bulletin_channel == "ceo_desk":
        notification_metadata["bulletin_channel"] = bulletin_channel
        OrgNotification.objects.create(
            title="MD & CEO's Desk updated",
            message=post.title,
            category="bulletin",
            target_tab="ceo-desk",
            metadata=notification_metadata,
            created_by_id=post.author_id,
        )
        return

    OrgNotification.objects.create(
        title=f"Company bulletin updated: {post.title}"[:180],
        message=(post.body or "")[:220],
        category="bulletin",
        target_tab="bulletin",
        metadata={**notification_metadata, "topic": post.topic},
        created_by_id=post.author_id,
    )


def backfill_today_org_notifications(apps, schema_editor):
    Post = apps.get_model("feed", "Post")
    OrgNotification = apps.get_model("operations", "OrgNotification")

    start = _today_start()
    posts = (
        Post.objects.filter(
            module="bulletin",
            visibility="company",
            moderation_status="published",
        )
        .filter(Q(updated_at__gte=start) | Q(published_at__gte=start) | Q(created_at__gte=start))
        .order_by("updated_at", "id")
    )
    for post in posts:
        _create_notification_for_post(OrgNotification, post)


class Migration(migrations.Migration):
    dependencies = [
        ("feed", "0020_update_cybersecurity_story_winners"),
        ("operations", "0008_org_notifications"),
    ]

    operations = [
        migrations.RunPython(
            backfill_today_org_notifications,
            migrations.RunPython.noop,
        ),
    ]
