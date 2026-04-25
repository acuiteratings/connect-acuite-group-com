from django.db import migrations
from django.utils import timezone


ANNOUNCEMENT_TITLE = "Important Update | SEBI Circular - What You Should Know"
ANNOUNCEMENT_BODY = (
    "SEBI's circular dated 10 February 2026 reinforces a key expectation from Credit Rating "
    "Agencies: clear distinction, transparency, and accountability while rating instruments "
    "governed by non-SEBI regulators. In line with this, necessary changes have been "
    "implemented in systems and processes.\n\n"
    "These changes directly impact how we represent our work and uphold regulatory trust - "
    "employees are encouraged to review the details available on the link below and stay "
    "informed."
)
ANNOUNCEMENT_META_LINE = "Effective Date: April 10, 2026"


def add_regulations_announcement(apps, schema_editor):
    Post = apps.get_model("feed", "Post")
    User = apps.get_model("accounts", "User")

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
        if str(metadata.get("home_announcement_tag", "")).strip().lower() == "regulations":
            existing_post = post
            break

    metadata = {
        "bulletin_category": "announcements",
        "bulletin_channel": "announcements",
        "home_announcement_tag": "regulations",
        "home_announcement_type": "other",
        "home_announcement_town_hall": None,
        "bulletin_meta_lines": [ANNOUNCEMENT_META_LINE],
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
        ("feed", "0006_update_town_hall_announcement_details"),
    ]

    operations = [
        migrations.RunPython(
            add_regulations_announcement,
            migrations.RunPython.noop,
        ),
    ]
