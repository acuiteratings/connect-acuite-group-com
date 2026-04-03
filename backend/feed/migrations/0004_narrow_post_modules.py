from django.db import migrations, models


def _community_submission_key(metadata, topic):
    community_type = str((metadata or {}).get("community_type") or "").strip().lower()
    topic = str(topic or "").strip().lower()
    if community_type == "looking_for_roommate" or topic == "housing":
        return "looking_for_roommate"
    if community_type == "giveaway":
        return "give_away"
    if community_type == "barter":
        return "exchange_something"
    if community_type == "sell":
        return "exchange_something"
    if topic == "marketplace":
        return "exchange_something"
    return "share_story"


def remap_post_modules(apps, schema_editor):
    Post = apps.get_model("feed", "Post")

    for post in Post.objects.all().iterator():
        metadata = dict(post.metadata or {})
        original_module = str(post.module or "").strip()
        topic = str(post.topic or "").strip().lower()
        new_topic = topic
        new_module = original_module or "bulletin"

        if original_module not in {"bulletin", "employee_posts"} and original_module:
            metadata.setdefault("legacy_module", original_module)

        if original_module == "community":
            new_module = "employee_posts"
            new_topic = "employee_submission"
            metadata.setdefault("bulletin_category", "employee_posts")
            metadata.setdefault("submission_key", _community_submission_key(metadata, topic))
            metadata.setdefault("submission_label", "Employee post")
        elif original_module == "ideas_voice":
            if topic == "ceo_corner":
                new_module = "bulletin"
                metadata.setdefault("bulletin_category", "announcements")
                metadata.setdefault("bulletin_channel", "ceo_desk")
            else:
                new_module = "employee_posts"
                new_topic = "employee_submission"
                metadata.setdefault("bulletin_category", "employee_posts")
                metadata.setdefault("submission_key", "share_idea")
                metadata.setdefault("submission_label", "I have an idea to share")
        elif original_module == "recognition":
            new_module = "employee_posts"
            new_topic = "employee_submission"
            metadata.setdefault("bulletin_category", "employee_posts")
            metadata.setdefault("submission_key", "praise_someone")
            metadata.setdefault("submission_label", "I want to praise someone")
        elif original_module == "general":
            if topic == "employee_submission":
                new_module = "employee_posts"
                metadata.setdefault("bulletin_category", "employee_posts")
            else:
                new_module = "bulletin"
                metadata.setdefault("bulletin_category", topic or "announcements")
        elif original_module in {"business", "clubs_learning"}:
            new_module = "bulletin"
            metadata.setdefault("bulletin_category", topic or "announcements")
        elif original_module not in {"bulletin", "employee_posts"}:
            if topic == "employee_submission":
                new_module = "employee_posts"
                metadata.setdefault("bulletin_category", "employee_posts")
            else:
                new_module = "bulletin"
                metadata.setdefault("bulletin_category", topic or "announcements")

        dirty = False
        if post.module != new_module:
            post.module = new_module
            dirty = True
        if post.topic != new_topic:
            post.topic = new_topic
            dirty = True
        if post.metadata != metadata:
            post.metadata = metadata
            dirty = True

        if dirty:
            post.save(update_fields=["module", "topic", "metadata", "updated_at"])


class Migration(migrations.Migration):
    dependencies = [
        ("feed", "0003_postreaction"),
    ]

    operations = [
        migrations.RunPython(remap_post_modules, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="post",
            name="module",
            field=models.CharField(
                choices=[
                    ("bulletin", "Bulletin Board"),
                    ("employee_posts", "Employee Posts"),
                ],
                default="bulletin",
                max_length=32,
            ),
        ),
    ]
