from django.db import migrations


def adjust_people_culture_yoga_poster_copy(apps, schema_editor):
    Post = apps.get_model("feed", "Post")

    existing_post = None
    for post in Post.objects.filter(module="bulletin", topic="announcements").order_by("-created_at"):
        metadata = dict(post.metadata or {})
        tag = str(metadata.get("home_announcement_tag", "")).strip().lower()
        if tag == "people_culture":
            existing_post = post
            break

    if not existing_post:
        return

    metadata = dict(existing_post.metadata or {})
    display = dict(metadata.get("home_announcement_display") or {})
    if not display:
        return

    display["details"] = [
        "Thank you to everyone who participated in the contest."
    ]
    display["closingNote"] = ""
    metadata["home_announcement_display"] = display
    existing_post.metadata = metadata
    existing_post.save(update_fields=["metadata", "updated_at"])


class Migration(migrations.Migration):
    dependencies = [
        ("feed", "0024_tighten_people_culture_yoga_winners_copy"),
    ]

    operations = [
        migrations.RunPython(
            adjust_people_culture_yoga_poster_copy,
            migrations.RunPython.noop,
        ),
    ]
