from django.db import migrations
from django.utils import timezone


ANNOUNCEMENT_TITLE = "Cybersecurity Awareness Drive 2026: 'Share Your Story' Winners"
ANNOUNCEMENT_BODY = (
    "Cybersecurity Awareness Drive 2026: 'Share Your Story' Winners\n\n"
    "We received many insightful stories about cyber-attacks, scams, and online fraud, where "
    "individuals successfully tackled challenges and navigated their way out.\n\n"
    "Thank you to everyone who participated and helped spread cyber awareness across the organization.\n\n"
    "Top 2 Story Winners are:\n\n"
    "1ST PLACE\n"
    "Disha Parekh\n\n"
    "The Story:\n"
    "While traveling between meetings, I received an email that appeared to be from our CEO, "
    "Sankar Chakraborti, asking me to complete a quick task and share my WhatsApp number. Although "
    "it looked genuine, I noticed the sender's email address was different. Suspecting a phishing "
    "attempt, I immediately reported it to the IT team, who confirmed it was a forged email and "
    "promptly blocked the malicious domains.\n\n"
    "The Lesson:\n"
    "Always verify unexpected requests, even if they appear to come from senior leadership. "
    "Cybersecurity awareness and staying alert to suspicious emails can prevent phishing attacks "
    "and protect both individuals and the organization.\n\n"
    "2ND PLACE\n"
    "Riddhi Chavan\n\n"
    "The story:\n"
    "My friend and I ordered clothes from an Instagram page that appeared genuine and paid in "
    "advance. Later, the seller demanded an extra ₹3,000 as “GST,” promising it would be refunded "
    "after delivery. Trusting the seller, we paid, but the clothes never arrived, no refund was "
    "given, and the seller disappeared.\n\n"
    "The lesson:\n"
    "The incident taught us to be cautious of fake online sellers, avoid unexpected payment requests, "
    "and verify businesses before making online purchases.\n\n"
    "Congratulations to both the winners! Your winning voucher shall be emailed to you soon."
)


def update_cybersecurity_story_winners(apps, schema_editor):
    Post = apps.get_model("feed", "Post")
    PostReaction = apps.get_model("feed", "PostReaction")
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
        "bulletin_meta_lines": ["Cybersecurity Awareness Drive 2026"],
        "home_announcement_display": {
            "formatLabel": "Share Your Story",
            "dateLabel": "2026 Drive",
            "timeLabel": "Winners announced",
            "venueLabel": "Connect",
            "hostLabel": "IT Team",
            "audienceLabel": "For all employees",
            "countdownLabel": "Congratulations to both winners",
            "summary": (
                "We received many insightful stories about cyber-attacks, scams, and online fraud, "
                "where individuals successfully tackled challenges and navigated their way out."
            ),
            "details": [
                "Thank you to everyone who participated and helped spread cyber awareness across the organization.",
                "Top 2 Story Winners are:",
            ],
            "closingNote": "Congratulations to both the winners! Your winning voucher shall be emailed to you soon.",
            "layoutVariant": "story_winners",
            "winners": [
                {
                    "place": "1st Place",
                    "name": "Disha Parekh",
                    "story": (
                        "While traveling between meetings, I received an email that appeared to be from our CEO, "
                        "Sankar Chakraborti, asking me to complete a quick task and share my WhatsApp number. "
                        "Although it looked genuine, I noticed the sender's email address was different. "
                        "Suspecting a phishing attempt, I immediately reported it to the IT team, who confirmed "
                        "it was a forged email and promptly blocked the malicious domains."
                    ),
                    "lesson": (
                        "Always verify unexpected requests, even if they appear to come from senior leadership. "
                        "Cybersecurity awareness and staying alert to suspicious emails can prevent phishing "
                        "attacks and protect both individuals and the organization."
                    ),
                },
                {
                    "place": "2nd Place",
                    "name": "Riddhi Chavan",
                    "story": (
                        "My friend and I ordered clothes from an Instagram page that appeared genuine and paid "
                        "in advance. Later, the seller demanded an extra ₹3,000 as “GST,” promising it would be "
                        "refunded after delivery. Trusting the seller, we paid, but the clothes never arrived, "
                        "no refund was given, and the seller disappeared."
                    ),
                    "lesson": (
                        "The incident taught us to be cautious of fake online sellers, avoid unexpected payment "
                        "requests, and verify businesses before making online purchases."
                    ),
                },
            ],
        },
        "post_as_company": True,
        "company_author_name": "IT Team",
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
        ("feed", "0019_update_people_culture_wellness_habits"),
    ]

    operations = [
        migrations.RunPython(
            update_cybersecurity_story_winners,
            migrations.RunPython.noop,
        ),
    ]
