from django.db import migrations
from django.utils import timezone


ANNOUNCEMENT_TITLE = "Submit your Investment Declaration on the HGS Portal for FY 2026-27"
ANNOUNCEMENT_BODY = (
    "HGS Portal for FY 2026-27 will open again next month. Those who have not yet submitted, "
    "please do so before the next salary cycle is closed. Portal link - https://ess.hgsbs.com. "
    "Important note: As mandated by Finance Act 2023, New Tax Regime will be the default regime "
    "for computing tax on salary income. In case of any queries feel free to write to the HR team "
    "at hrsupport@acuite.in."
)
ANNOUNCEMENT_META_LINE = "Portal: https://ess.hgsbs.com"


def add_people_culture_announcement(apps, schema_editor):
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
        if str(metadata.get("home_announcement_tag", "")).strip().lower() == "people_culture":
            existing_post = post
            break

    metadata = {
        "bulletin_category": "announcements",
        "bulletin_channel": "announcements",
        "home_announcement_tag": "people_culture",
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
        ("feed", "0008_add_giving_announcement"),
    ]

    operations = [
        migrations.RunPython(
            add_people_culture_announcement,
            migrations.RunPython.noop,
        ),
    ]
