from django.db import migrations
from django.utils import timezone


ANNOUNCEMENT_TITLE = "Trading Advisory 1"
ANNOUNCEMENT_BODY = (
    "Dear Acuiteans,\n\n"
    "While seeking trading approval on STAMP, employees are required to enter the "
    "complete/correct name of the company they want to trade in. Pls. refrain from "
    "using stock symbols/incomplete company name while seeking approvals. If you have "
    "any queries in this regard, pls. reach out to Enaakshi Majumdar from Compliance "
    "Team at enaakshi.majumdar@acuite.in."
)
ANNOUNCEMENT_SUMMARY = (
    "Dear Acuiteans, while seeking trading approval on STAMP, employees are required "
    "to enter the complete/correct name of the company they want to trade in. Pls. "
    "refrain from using stock symbols/incomplete company name while seeking approvals. "
    "If you have any queries in this regard, pls. reach out to Enaakshi Majumdar from "
    "Compliance Team at enaakshi.majumdar@acuite.in."
)


def update_compliance_announcement(apps, schema_editor):
    Post = apps.get_model("feed", "Post")
    User = apps.get_model("accounts", "User")

    existing_post = None
    for post in Post.objects.filter(module="bulletin", topic="announcements").order_by("-created_at"):
        metadata = dict(post.metadata or {})
        tag = str(metadata.get("home_announcement_tag", "")).strip().lower()
        if tag == "compliance":
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
        "home_announcement_tag": "compliance",
        "home_announcement_type": "other",
        "home_announcement_town_hall": None,
        "bulletin_meta_lines": ["STAMP trading approval advisory"],
        "home_announcement_display": {
            "formatLabel": "STAMP",
            "dateLabel": "Now live",
            "timeLabel": "Before seeking trading approval",
            "venueLabel": "STAMP Portal",
            "hostLabel": "Compliance Team",
            "audienceLabel": "Mode: Online",
            "countdownLabel": "Contact: enaakshi.majumdar@acuite.in",
            "summary": ANNOUNCEMENT_SUMMARY,
        },
        "post_as_company": True,
        "company_author_name": "Compliance Team",
        "company_author_title": "Official company post",
        "company_author_initials": "CT",
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
        ("feed", "0016_update_people_culture_nuclear_seminar"),
    ]

    operations = [
        migrations.RunPython(
            update_compliance_announcement,
            migrations.RunPython.noop,
        ),
    ]
