from django.db import migrations


ANNOUNCEMENT_UPDATES = {
    "people_culture": {
        "label": "People & Culture",
        "message": "International Yoga Day Celebration - Event Feedback",
    },
    "new_initiatives": {
        "label": "New Initiatives",
        "message": "Myself Application - Beta Launch",
    },
}


def backfill_june22_announcement_notifications(apps, schema_editor):
    Post = apps.get_model("feed", "Post")
    OrgNotification = apps.get_model("operations", "OrgNotification")

    for tag, config in ANNOUNCEMENT_UPDATES.items():
        post = None
        for candidate in Post.objects.filter(module="bulletin", topic="announcements").order_by("-created_at"):
            metadata = dict(candidate.metadata or {})
            if str(metadata.get("home_announcement_tag", "")).strip().lower() == tag:
                post = candidate
                break

        if not post:
            continue

        already_exists = OrgNotification.objects.filter(
            category="announcement",
            title=f"{config['label']} announcement updated",
            message=config["message"],
            metadata__source="june_22_announcement_backfill",
            metadata__home_announcement_filter=tag,
        ).exists()
        if already_exists:
            continue

        OrgNotification.objects.create(
            title=f"{config['label']} announcement updated",
            message=config["message"],
            category="announcement",
            target_tab="home",
            metadata={
                "post_id": post.id,
                "source_post_id": post.id,
                "home_announcement_filter": tag,
                "source": "june_22_announcement_backfill",
            },
            created_by_id=post.author_id,
        )


class Migration(migrations.Migration):
    dependencies = [
        ("feed", "0021_update_new_initiatives_myself_beta_launch"),
        ("operations", "0009_backfill_today_org_notifications"),
    ]

    operations = [
        migrations.RunPython(
            backfill_june22_announcement_notifications,
            migrations.RunPython.noop,
        ),
    ]
