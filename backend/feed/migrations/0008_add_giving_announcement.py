from django.db import migrations
from django.utils import timezone


ANNOUNCEMENT_TITLE = "Together for Vatsalya - Small hands, Big smiles!"
ANNOUNCEMENT_BODY = (
    "We are associated with Vatsalya Trust as part of our CSR initiatives, supporting "
    "their care for infants, newborns, and specially abled children. Employees who "
    "would like to be part of this meaningful cause may contribute either through "
    "donations in kind or by coming together in groups to spend quality time with the "
    "children.\n\n"
    "Small gestures can make a lasting difference in their lives. We encourage all "
    "interested colleagues to join and support this initiative.\n\n"
    "Place: Kanjurmarg East"
)
ANNOUNCEMENT_META_LINE = "Place: Kanjurmarg East"


def add_giving_announcement(apps, schema_editor):
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
        if str(metadata.get("home_announcement_tag", "")).strip().lower() == "giving":
            existing_post = post
            break

    metadata = {
        "bulletin_category": "announcements",
        "bulletin_channel": "announcements",
        "home_announcement_tag": "giving",
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
        ("feed", "0007_add_regulations_announcement"),
    ]

    operations = [
        migrations.RunPython(
            add_giving_announcement,
            migrations.RunPython.noop,
        ),
    ]
