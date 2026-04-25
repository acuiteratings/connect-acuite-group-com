from django.db import migrations
from django.utils import timezone


CYBER_TITLE = "Cybersecurity Essentials: Employee Awareness Session"
CYBER_BODY = (
    "This session will cover the most important practices to protect your devices, data, "
    "and privacy at work, use of AI, latest cybercrime & many more. Whether you're a "
    "beginner or just want a refresher, join us to strengthen your cyber defences. Let's "
    "make IT Security everyone's responsibility!"
)


def apply_announcement_updates(apps, schema_editor):
    Post = apps.get_model("feed", "Post")
    User = apps.get_model("accounts", "User")

    for post in Post.objects.filter(module="bulletin", topic="announcements").iterator():
        metadata = dict(post.metadata or {})
        tag = str(metadata.get("home_announcement_tag", "")).strip().lower()
        if tag != "giving":
            continue

        metadata["bulletin_meta_lines"] = ["17 May 2026"]
        metadata["home_announcement_display"] = {
            "formatLabel": "CSR",
            "dateLabel": "17 May 2026",
            "timeLabel": "Open for employee participation",
            "venueLabel": "Kanjurmarg East",
            "hostLabel": "Vatsalya Trust",
            "audienceLabel": "Open to interested employees",
            "countdownLabel": "Donations in kind or time with the children",
        }
        post.metadata = metadata
        post.save(update_fields=["metadata", "updated_at"])

    author = (
        User.objects.filter(
            is_active=True,
            employment_status="active",
            access_level="admin",
        )
        .order_by("id")
        .first()
    ) or User.objects.filter(is_active=True).order_by("id").first()

    if not author:
        return

    existing_post = None
    for post in Post.objects.filter(module="bulletin", topic="announcements").order_by("-created_at"):
        metadata = dict(post.metadata or {})
        if str(metadata.get("home_announcement_tag", "")).strip().lower() == "cybersecurity":
            existing_post = post
            break

    metadata = {
        "bulletin_category": "announcements",
        "bulletin_channel": "announcements",
        "home_announcement_tag": "cybersecurity",
        "home_announcement_type": "other",
        "home_announcement_town_hall": None,
        "bulletin_meta_lines": ["May 15, 2026"],
        "home_announcement_display": {
            "formatLabel": "Online",
            "dateLabel": "May 15, 2026",
            "timeLabel": "Employee awareness session",
            "venueLabel": "MS Teams",
            "hostLabel": "IT Team",
            "audienceLabel": "Mode: Online",
            "countdownLabel": "IT Security is everyone's responsibility",
            "summary": CYBER_BODY,
        },
        "post_as_company": True,
        "company_author_name": "IT Team",
        "company_author_title": "Official company post",
        "company_author_initials": "IT",
    }

    if existing_post:
        existing_post.title = CYBER_TITLE
        existing_post.body = CYBER_BODY
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
        title=CYBER_TITLE,
        body=CYBER_BODY,
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
        ("feed", "0009_add_people_culture_announcement"),
    ]

    operations = [
        migrations.RunPython(
            apply_announcement_updates,
            migrations.RunPython.noop,
        ),
    ]
