from django.db import migrations
from django.utils import timezone


ANNOUNCEMENT_TITLE = "Townhall – Q1 FY 2027:"
ANNOUNCEMENT_BODY = (
    "Join us for an overview of the key updates from the first quarter and insights "
    "into the priorities and plans for the months ahead."
)
ANNOUNCEMENT_DATE = "July 14, 2026"
ANNOUNCEMENT_TIME = "10.30 am IST"
ANNOUNCEMENT_WHERE = "Stay tuned"
ANNOUNCEMENT_HOST = "MD & CEO with the leadership team"
ANNOUNCEMENT_JOIN_URL = "https://teams.microsoft.com/meet/47214103486887?p=nAybmcJksELWmn2AIJ"
ANNOUNCEMENT_MEETING_ID = "472 141 034 868 87"
ANNOUNCEMENT_PASSCODE = "hK9Fq7P2"


def add_leadership_townhall_join_details(apps, schema_editor):
    Post = apps.get_model("feed", "Post")
    User = apps.get_model("accounts", "User")

    existing_post = None
    for post in Post.objects.filter(module="bulletin", topic="announcements").order_by("-created_at"):
        metadata = dict(post.metadata or {})
        tag = str(metadata.get("home_announcement_tag", "")).strip().lower()
        announcement_type = str(metadata.get("home_announcement_type", "")).strip().lower()
        if tag == "leadership" or announcement_type == "town_hall":
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
        "home_announcement_tag": "leadership",
        "home_announcement_type": "other",
        "home_announcement_town_hall": None,
        "bulletin_meta_lines": [f"{ANNOUNCEMENT_DATE} | {ANNOUNCEMENT_TIME}"],
        "bulletin_cta_label": "Join on Microsoft Teams",
        "bulletin_cta_target": ANNOUNCEMENT_JOIN_URL,
        "home_announcement_display": {
            "typeLabel": "Townhall",
            "formatLabel": "Q1 FY 2027",
            "dateLabel": ANNOUNCEMENT_DATE,
            "timeLabel": ANNOUNCEMENT_TIME,
            "venueLabel": ANNOUNCEMENT_WHERE,
            "hostLabel": ANNOUNCEMENT_HOST,
            "audienceLabel": "Open to all employees",
            "countdownLabel": "Priorities and plans for the months ahead",
            "summary": ANNOUNCEMENT_BODY,
            "ctaLabel": "Join on Microsoft Teams",
            "ctaTarget": ANNOUNCEMENT_JOIN_URL,
            "details": [
                f"Join: {ANNOUNCEMENT_JOIN_URL}",
                f"Meeting ID: {ANNOUNCEMENT_MEETING_ID}",
                f"Passcode: {ANNOUNCEMENT_PASSCODE}",
            ],
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
        ("feed", "0028_update_leadership_townhall_time"),
    ]

    operations = [
        migrations.RunPython(
            add_leadership_townhall_join_details,
            migrations.RunPython.noop,
        ),
    ]
