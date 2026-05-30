from django.db import migrations
from django.utils import timezone


ANNOUNCEMENT_TITLE = "Wellness at Work: Healthy Habits for a Productive Day"
ANNOUNCEMENT_BODY = (
    "Productivity is often supported by simple habits and the effective use of available tools.\n\n"
    "It is important to manage the workday in a structured manner — respond to emails at planned "
    "intervals, avoid unnecessary multitasking, reduce distractions, take short screen breaks, "
    "and keep frequently used files / information well organised. Simple wellness practices such "
    "as staying hydrated, maintaining good posture, and taking brief pauses between long tasks "
    "can help sustain energy through the day.\n\n"
    "By combining healthy work habits with smart tools, you can manage time better, reduce "
    "avoidable stress, and work more effectively."
)
ANNOUNCEMENT_SUMMARY = (
    "Productivity is often supported by simple habits and the effective use of available tools."
)
ANNOUNCEMENT_DETAILS = [
    (
        "It is important to manage the workday in a structured manner — respond to emails at "
        "planned intervals, avoid unnecessary multitasking, reduce distractions, take short screen "
        "breaks, and keep frequently used files / information well organised."
    ),
    (
        "Simple wellness practices such as staying hydrated, maintaining good posture, and taking "
        "brief pauses between long tasks can help sustain energy through the day."
    ),
    (
        "By combining healthy work habits with smart tools, you can manage time better, reduce "
        "avoidable stress, and work more effectively."
    ),
]


def update_people_culture_wellness_announcement(apps, schema_editor):
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
        "bulletin_meta_lines": ["Wellness at work"],
        "home_announcement_display": {
            "formatLabel": "Wellness",
            "dateLabel": "Now live",
            "timeLabel": "Healthy workday habits",
            "venueLabel": "Connect",
            "hostLabel": "People & Culture",
            "audienceLabel": "For all employees",
            "countdownLabel": "Small habits, better workdays",
            "summary": ANNOUNCEMENT_SUMMARY,
            "details": ANNOUNCEMENT_DETAILS,
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
        ("feed", "0018_reset_people_culture_reactions"),
    ]

    operations = [
        migrations.RunPython(
            update_people_culture_wellness_announcement,
            migrations.RunPython.noop,
        ),
    ]
