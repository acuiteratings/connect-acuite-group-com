from django.db import migrations
from django.utils import timezone


ANNOUNCEMENT_TITLE = "Cybersecurity Essentials: Assess Your Awareness"
ANNOUNCEMENT_LINK = "https://forms.office.com/r/DvZ2mHS27t"
ANNOUNCEMENT_BODY = (
    "Take this quick 10-minute assessment using the link below to evaluate your "
    "cybersecurity awareness. Participation is mandatory for all employees. "
    f"Link: {ANNOUNCEMENT_LINK}"
)
ANNOUNCEMENT_WHEN = "Last Date - May 25, 2026"
ANNOUNCEMENT_WHERE = "Microsoft Forms | Online"
ANNOUNCEMENT_HOST = "IT Team"
ANNOUNCEMENT_HOST_NOTE = "Cybersecurity is everyone's responsibility."


def update_cybersecurity_announcement(apps, schema_editor):
    Post = apps.get_model("feed", "Post")
    User = apps.get_model("accounts", "User")

    existing_post = None
    for post in Post.objects.filter(module="bulletin", topic="announcements").order_by("-created_at"):
        metadata = dict(post.metadata or {})
        tag = str(metadata.get("home_announcement_tag", "")).strip().lower()
        if tag == "cybersecurity":
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
        "home_announcement_tag": "cybersecurity",
        "home_announcement_type": "other",
        "home_announcement_town_hall": None,
        "bulletin_meta_lines": [ANNOUNCEMENT_WHEN],
        "bulletin_cta_label": "Open assessment",
        "bulletin_cta_target": ANNOUNCEMENT_LINK,
        "home_announcement_display": {
            "formatLabel": "Assessment",
            "dateLabel": "May 25, 2026",
            "timeLabel": "Last Date",
            "venueLabel": ANNOUNCEMENT_WHERE,
            "hostLabel": ANNOUNCEMENT_HOST,
            "audienceLabel": "Mandatory for all employees",
            "countdownLabel": ANNOUNCEMENT_HOST_NOTE,
            "summary": ANNOUNCEMENT_BODY,
            "ctaLabel": "Open assessment",
            "ctaTarget": ANNOUNCEMENT_LINK,
        },
        "post_as_company": True,
        "company_author_name": ANNOUNCEMENT_HOST,
        "company_author_title": "Official company post",
        "company_author_initials": "IT",
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
        ("feed", "0013_update_new_initiatives_idea_announcement"),
    ]

    operations = [
        migrations.RunPython(
            update_cybersecurity_announcement,
            migrations.RunPython.noop,
        ),
    ]
