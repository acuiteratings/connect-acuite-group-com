from django.db import migrations
from django.utils import timezone


ANNOUNCEMENT_TITLE = "Myself Application - Beta Launch"
ANNOUNCEMENT_BODY = (
    "We’re delighted to announce the beta launch of the 'Myself' Application. A new platform "
    "designed to simplify and unify our leave and attendance processes.\n\n"
    "Key highlights:\n"
    "- Track your daily attendance directly in the Myself application.\n"
    "- Submit requests for WFH, Travel, or Leave in Myself Application.\n\n"
    "Please read the detailed launch email for complete instructions, next steps, and support "
    "contacts.\n\n"
    "Your feedback during this beta phase is crucial to refining the system and ensuring a smooth "
    "rollout. Write to hrsupport@acuite.in for queries, if any.\n\n"
    "In coordination with App & HR Team"
)
ANNOUNCEMENT_SUMMARY = (
    "We’re delighted to announce the beta launch of the 'Myself' Application, a new platform "
    "designed to simplify and unify our leave and attendance processes."
)
ANNOUNCEMENT_DETAILS = [
    "Track your daily attendance directly in the Myself application.",
    "Submit requests for WFH, Travel, or Leave in Myself Application.",
    "Please read the detailed launch email for complete instructions, next steps, and support contacts.",
    (
        "Your feedback during this beta phase is crucial to refining the system and ensuring a smooth "
        "rollout. Write to hrsupport@acuite.in for queries, if any."
    ),
]


def update_new_initiatives_myself_beta_launch(apps, schema_editor):
    Post = apps.get_model("feed", "Post")
    PostReaction = apps.get_model("feed", "PostReaction")
    User = apps.get_model("accounts", "User")

    existing_post = None
    for post in Post.objects.filter(module="bulletin", topic="announcements").order_by("-created_at"):
        metadata = dict(post.metadata or {})
        tag = str(metadata.get("home_announcement_tag", "")).strip().lower()
        if tag == "new_initiatives":
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
        "home_announcement_tag": "new_initiatives",
        "home_announcement_type": "other",
        "home_announcement_town_hall": None,
        "bulletin_meta_lines": ["Now live | Myself Application | App & HR Team"],
        "home_announcement_display": {
            "formatLabel": "Beta Launch",
            "dateLabel": "Now live",
            "timeLabel": "Leave and attendance in one place",
            "venueLabel": "Myself Application",
            "hostLabel": "App & HR Team",
            "audienceLabel": "For all employees",
            "countdownLabel": "Write to hrsupport@acuite.in for queries",
            "summary": ANNOUNCEMENT_SUMMARY,
            "details": ANNOUNCEMENT_DETAILS,
        },
        "post_as_company": True,
        "company_author_name": "Acuite Ratings & Research",
        "company_author_title": "Official company post",
        "company_author_initials": "AR",
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
        ("feed", "0020_update_cybersecurity_story_winners"),
    ]

    operations = [
        migrations.RunPython(
            update_new_initiatives_myself_beta_launch,
            migrations.RunPython.noop,
        ),
    ]
