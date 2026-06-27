from django.db import migrations
from django.utils import timezone


ANNOUNCEMENT_TITLE = "International Yoga Day Celebration - Winners"
ANNOUNCEMENT_BODY = (
    "Congratulations to Pranay Sail, Akshita Chawda, and Kaustubh Patil for winning the "
    "Yoga Pose Competition.\n\nPlease see the winners poster below."
)
ANNOUNCEMENT_SUMMARY = (
    "Congratulations to Pranay Sail, Akshita Chawda, and Kaustubh Patil for winning the "
    "Yoga Pose Competition."
)
ANNOUNCEMENT_DETAILS = [
    "Please see the winners poster below.",
]
ANNOUNCEMENT_IMAGE_URL = "/static/img/yoga-pose-winners-june-2026.jpg"
ANNOUNCEMENT_IMAGE_ALT = (
    "Yoga Pose Competition winners poster featuring Pranay Sail, Akshita Chawda, and Kaustubh Patil."
)


def update_people_culture_yoga_winners(apps, schema_editor):
    Post = apps.get_model("feed", "Post")
    PostReaction = apps.get_model("feed", "PostReaction")
    User = apps.get_model("accounts", "User")

    existing_post = None
    for post in Post.objects.filter(module="bulletin", topic="announcements").order_by("-created_at"):
        metadata = dict(post.metadata or {})
        tag = str(metadata.get("home_announcement_tag", "")).strip().lower()
        if tag == "people_culture":
            existing_post = post
            break

    author = (
        User.objects.filter(
            is_active=True,
            employment_status="active",
            access_level="admin",
        )
        .order_by("id")
        .first()
    ) or User.objects.filter(is_active=True).order_by("id").first()

    if not existing_post and not author:
        return

    metadata = {
        "bulletin_category": "announcements",
        "bulletin_channel": "announcements",
        "home_announcement_tag": "people_culture",
        "home_announcement_type": "other",
        "home_announcement_town_hall": None,
        "bulletin_meta_lines": ["Now live | Yoga Pose Competition | People & Culture"],
        "bulletin_image_url": ANNOUNCEMENT_IMAGE_URL,
        "bulletin_image_alt": ANNOUNCEMENT_IMAGE_ALT,
        "home_announcement_display": {
            "formatLabel": "Winners",
            "dateLabel": "Now live",
            "timeLabel": "Yoga Pose Competition",
            "venueLabel": "Connect",
            "hostLabel": "People & Culture",
            "audienceLabel": "For all employees",
            "countdownLabel": "Congratulations to all our winners",
            "summary": ANNOUNCEMENT_SUMMARY,
            "details": ANNOUNCEMENT_DETAILS,
            "imageUrl": ANNOUNCEMENT_IMAGE_URL,
            "imageAlt": ANNOUNCEMENT_IMAGE_ALT,
            "imageStyle": "poster",
        },
        "post_as_company": True,
        "company_author_name": "People & Culture",
        "company_author_title": "Official company post",
        "company_author_initials": "PC",
    }

    if existing_post:
        existing_post.title = ANNOUNCEMENT_TITLE
        existing_post.body = ANNOUNCEMENT_BODY
        existing_post.kind = "announcement"
        existing_post.module = "bulletin"
        existing_post.topic = "announcements"
        existing_post.visibility = "company"
        existing_post.moderation_status = "published"
        existing_post.allow_comments = True
        existing_post.metadata = metadata
        if not existing_post.published_at:
            existing_post.published_at = timezone.now()
        existing_post.save()
        PostReaction.objects.filter(post=existing_post).delete()
        return

    Post.objects.create(
        author=author,
        title=ANNOUNCEMENT_TITLE,
        body=ANNOUNCEMENT_BODY,
        kind="announcement",
        module="bulletin",
        topic="announcements",
        visibility="company",
        moderation_status="published",
        allow_comments=True,
        published_at=timezone.now(),
        metadata=metadata,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("feed", "0021_update_new_initiatives_myself_beta_launch"),
    ]

    operations = [
        migrations.RunPython(
            update_people_culture_yoga_winners,
            migrations.RunPython.noop,
        ),
    ]
