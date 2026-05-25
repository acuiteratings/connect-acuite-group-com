from django.db import migrations
from django.utils import timezone


ANNOUNCEMENT_TITLE = "Nuclear Technology Advancements in India"
REGISTRATION_LINK = "https://forms.gle/bjB29pSmAnR17bt97"
VENUE_LINK = "https://maps.app.goo.gl/3tertz8HfBDN7V48A"
ANNOUNCEMENT_BODY = (
    'With the successful progress of the "PFBR Kalpakkam Project", India is taking a '
    "significant leap toward self-reliance and advanced nuclear innovation.\n\n"
    'The "Seva Sahayog Science Forum" (Acuite’s CSR Partner) invites students, educators, '
    "researchers, academicians, and science enthusiasts to an engaging and insightful seminar on:\n\n"
    "Nuclear Technology Advancements in India\n"
    f"Registration Link Here: {REGISTRATION_LINK}\n\n"
    "Date: Saturday, 30 May 2026\n"
    "Time: 10:00 AM - 1:00 PM\n"
    f"Venue: Ramnarain Ruia Autonomous College, Matunga East, Mumbai - 400019 {VENUE_LINK}\n\n"
    "Seminar Highlights\n\n"
    "Fundamentals of Nuclear Science & Technologies Focus on Nuclear Reactors\n"
    "India’s Current Position in Nuclear Science & Technology\n"
    "Bharat’s Policies & Roadmap Towards Nuclear Energy\n"
    "Career Opportunities in Nuclear Science & Research"
)
ANNOUNCEMENT_SUMMARY = (
    'With the successful progress of the "PFBR Kalpakkam Project", India is taking a '
    "significant leap toward self-reliance and advanced nuclear innovation. "
    'The "Seva Sahayog Science Forum" invites students, educators, researchers, '
    "academicians, and science enthusiasts to an engaging seminar on nuclear technology "
    "advancements in India."
)
ANNOUNCEMENT_DETAILS = [
    "Registration Link Here: https://forms.gle/bjB29pSmAnR17bt97",
    "Seminar Highlights",
    "Fundamentals of Nuclear Science & Technologies Focus on Nuclear Reactors",
    "India’s Current Position in Nuclear Science & Technology",
    "Bharat’s Policies & Roadmap Towards Nuclear Energy",
    "Career Opportunities in Nuclear Science & Research",
]


def update_people_culture_announcement(apps, schema_editor):
    Post = apps.get_model("feed", "Post")
    User = apps.get_model("accounts", "User")

    existing_post = None
    for post in Post.objects.filter(module="bulletin", topic="announcements").order_by("-created_at"):
        metadata = dict(post.metadata or {})
        tag = str(metadata.get("home_announcement_tag", "")).strip().lower()
        if tag == "people_culture":
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
        "home_announcement_tag": "people_culture",
        "home_announcement_type": "other",
        "home_announcement_town_hall": None,
        "bulletin_meta_lines": [
            "Saturday, 30 May 2026 | 10:00 AM - 1:00 PM",
            "Ramnarain Ruia Autonomous College, Matunga East, Mumbai - 400019",
        ],
        "bulletin_cta_label": "Register here",
        "bulletin_cta_target": REGISTRATION_LINK,
        "home_announcement_display": {
            "formatLabel": "Seminar",
            "dateLabel": "30 May 2026",
            "timeLabel": "Saturday | 10:00 AM - 1:00 PM",
            "venueLabel": "Ramnarain Ruia Autonomous College",
            "hostLabel": "Seva Sahayog Science Forum",
            "audienceLabel": "Matunga East, Mumbai - 400019",
            "countdownLabel": "Acuité’s CSR Partner",
            "summary": ANNOUNCEMENT_SUMMARY,
            "details": ANNOUNCEMENT_DETAILS,
            "ctaLabel": "Register here",
            "ctaTarget": REGISTRATION_LINK,
        },
        "post_as_company": True,
        "company_author_name": "People & Culture",
        "company_author_title": "Official company post",
        "company_author_initials": "PC",
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
        ("feed", "0015_extend_cybersecurity_assessment_deadline"),
    ]

    operations = [
        migrations.RunPython(
            update_people_culture_announcement,
            migrations.RunPython.noop,
        ),
    ]
