from django.db import migrations


def reset_people_culture_reactions(apps, schema_editor):
    Post = apps.get_model("feed", "Post")
    PostReaction = apps.get_model("feed", "PostReaction")

    post_ids = []
    for post in Post.objects.filter(module="bulletin", topic="announcements"):
        metadata = dict(post.metadata or {})
        tag = str(metadata.get("home_announcement_tag", "")).strip().lower()
        if tag == "people_culture":
            post_ids.append(post.id)

    if post_ids:
        PostReaction.objects.filter(post_id__in=post_ids).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("feed", "0017_update_compliance_trading_advisory"),
    ]

    operations = [
        migrations.RunPython(
            reset_people_culture_reactions,
            migrations.RunPython.noop,
        ),
    ]
