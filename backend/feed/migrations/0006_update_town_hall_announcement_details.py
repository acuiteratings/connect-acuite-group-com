from django.db import migrations


NEW_TOWN_HALL_DATE = "2026-05-05"
NEW_TOWN_HALL_TIME = "6:00 PM onwards"
NEW_TOWN_HALL_VENUE = "The Rooftop & Malabar, Trident, Nariman Point."
NEW_TOWN_HALL_META_LINE = "Tuesday, 5th May 2026"


def update_town_hall_announcement_details(apps, schema_editor):
    Post = apps.get_model("feed", "Post")

    for post in Post.objects.filter(module="bulletin", topic="announcements").iterator():
        metadata = dict(post.metadata or {})
        if str(metadata.get("home_announcement_type", "")).strip() != "town_hall":
            continue

        town_hall_details = metadata.get("home_announcement_town_hall")
        if not isinstance(town_hall_details, dict):
            continue

        metadata["home_announcement_town_hall"] = {
            **town_hall_details,
            "date": NEW_TOWN_HALL_DATE,
            "time": NEW_TOWN_HALL_TIME,
            "venue": NEW_TOWN_HALL_VENUE,
        }
        metadata["bulletin_meta_lines"] = [NEW_TOWN_HALL_META_LINE]

        post.metadata = metadata
        post.save(update_fields=["metadata", "updated_at"])


class Migration(migrations.Migration):
    dependencies = [
        ("feed", "0005_refresh_celebration_card_meta"),
    ]

    operations = [
        migrations.RunPython(
            update_town_hall_announcement_details,
            migrations.RunPython.noop,
        ),
    ]
