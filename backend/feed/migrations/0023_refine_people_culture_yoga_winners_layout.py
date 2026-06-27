from django.db import migrations


ANNOUNCEMENT_IMAGE_URL = "/static/img/yoga-pose-winners-june-2026.jpg"
ANNOUNCEMENT_IMAGE_ALT = (
    "Yoga Pose Competition winners poster featuring Pranay Sail, Akshita Chawda, and Kaustubh Patil."
)


def refine_people_culture_yoga_winners_layout(apps, schema_editor):
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
    metadata["bulletin_image_url"] = ANNOUNCEMENT_IMAGE_URL
    metadata["bulletin_image_alt"] = ANNOUNCEMENT_IMAGE_ALT
    metadata["home_announcement_display"] = {
        "formatLabel": "Winners",
        "dateLabel": "Now live",
        "timeLabel": "Top 3 winning poses",
        "venueLabel": "Connect",
        "hostLabel": "People & Culture",
        "audienceLabel": "For all employees",
        "countdownLabel": "Congratulations to all our winners",
        "summary": (
            "Congratulations to Pranay Sail, Akshita Chawda, and Kaustubh Patil for standing out in the "
            "Yoga Pose Competition."
        ),
        "details": [
            "Here are the three winning poses from the competition."
        ],
        "layoutVariant": "pose_winners",
        "winners": [
            {
                "place": "1st Place",
                "name": "Pranay Sail",
                "imageUrl": ANNOUNCEMENT_IMAGE_URL,
                "imagePosition": "6% 76%",
                "imageSize": "320% auto",
            },
            {
                "place": "2nd Place",
                "name": "Akshita Chawda",
                "imageUrl": ANNOUNCEMENT_IMAGE_URL,
                "imagePosition": "50% 76%",
                "imageSize": "320% auto",
            },
            {
                "place": "3rd Place",
                "name": "Kaustubh Patil",
                "imageUrl": ANNOUNCEMENT_IMAGE_URL,
                "imagePosition": "94% 76%",
                "imageSize": "320% auto",
            },
        ],
        "closingNote": "Thank you to everyone who participated and made the celebration special.",
    }

    existing_post.metadata = metadata
    existing_post.save(update_fields=["metadata", "updated_at"])


class Migration(migrations.Migration):
    dependencies = [
        ("feed", "0022_update_people_culture_yoga_winners"),
    ]

    operations = [
        migrations.RunPython(
            refine_people_culture_yoga_winners_layout,
            migrations.RunPython.noop,
        ),
    ]
