from django.db import migrations
from django.utils import timezone


ANNOUNCEMENT_TITLE = "Nominate your colleague for the Annual CEO Awards"
ANNOUNCEMENT_BODY = (
    "We are launching our annual awards, a long time demand from the employees. Here is the "
    "opportunity for you to nominate anyone who did an exemplary job in any area. If you know "
    "such people and the great work they have done, please do not hesitate. Nominate them.\n\n"
    "Go to My Posts and select I want to praise someone to post a message on the Bulletin Board. "
    "Others can also like and comment on your post.\n\n"
    "The best nominations will be shortlisted and added to the evaluation list for the HR "
    "committee's decision."
)
ANNOUNCEMENT_META_LINE = "Last date for nomination: 30 April 2026"


def add_new_initiatives_announcement(apps, schema_editor):
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
        if str(metadata.get("home_announcement_tag", "")).strip().lower() == "new_initiatives":
            existing_post = post
            break

    metadata = {
        "bulletin_category": "announcements",
        "bulletin_channel": "announcements",
        "home_announcement_tag": "new_initiatives",
        "home_announcement_type": "other",
        "home_announcement_town_hall": None,
        "bulletin_meta_lines": [ANNOUNCEMENT_META_LINE],
        "home_announcement_display": {
            "formatLabel": "Recognition",
            "dateLabel": ANNOUNCEMENT_META_LINE,
            "timeLabel": "Open now on Connect",
            "venueLabel": "My Posts > I want to praise someone",
            "hostLabel": "HR Committee",
            "audienceLabel": "Open to all employees",
            "countdownLabel": "Best nominations will be shortlisted for evaluation",
            "summary": ANNOUNCEMENT_BODY,
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
        ("feed", "0010_update_giving_and_add_cybersecurity_announcement"),
    ]

    operations = [
        migrations.RunPython(
            add_new_initiatives_announcement,
            migrations.RunPython.noop,
        ),
    ]
