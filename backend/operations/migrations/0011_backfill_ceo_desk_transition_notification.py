from django.db import migrations


CEO_DESK_TITLE = "Leadership Transition at Acuite"
NOTIFICATION_TITLE = "MD & CEO's Desk updated"
NOTIFICATION_SOURCE = "ceo_desk_transition_backfill"


def backfill_ceo_desk_transition_notification(apps, schema_editor):
    Post = apps.get_model("feed", "Post")
    OrgNotification = apps.get_model("operations", "OrgNotification")

    post = (
        Post.objects.filter(
            module="bulletin",
            topic="announcements",
            title=CEO_DESK_TITLE,
            metadata__bulletin_channel="ceo_desk",
        )
        .order_by("-created_at")
        .first()
    )
    if not post:
        return

    already_exists = OrgNotification.objects.filter(
        title=NOTIFICATION_TITLE,
        category="bulletin",
        message=post.title,
        target_tab="ceo-desk",
        metadata__post_id=post.id,
    ).exists() or OrgNotification.objects.filter(
        title=NOTIFICATION_TITLE,
        category="bulletin",
        message=post.title,
        metadata__source=NOTIFICATION_SOURCE,
        metadata__source_post_id=post.id,
    ).exists()
    if already_exists:
        return

    OrgNotification.objects.create(
        title=NOTIFICATION_TITLE,
        message=post.title,
        category="bulletin",
        target_tab="ceo-desk",
        metadata={
            "post_id": post.id,
            "source_post_id": post.id,
            "bulletin_channel": "ceo_desk",
            "source": NOTIFICATION_SOURCE,
        },
        created_by_id=post.author_id,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("feed", "0027_publish_ceo_desk_leadership_transition"),
        ("operations", "0010_backfill_june22_announcement_notifications"),
    ]

    operations = [
        migrations.RunPython(
            backfill_ceo_desk_transition_notification,
            migrations.RunPython.noop,
        ),
    ]
