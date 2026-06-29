from django.db import migrations
from django.utils import timezone


CEO_DESK_TITLE = "Leadership Transition at Acuite"
CEO_DESK_BODY = (
    "Dear colleagues,\n\n"
    "I am pleased to inform you that Mr. Pankaj Bansal will be joining Acuite Ratings & Research Limited "
    "tomorrow, June 30, 2026. He will assume charge as MD & CEO of Acuite effective July 15, 2026.\n\n"
    "Pankaj brings with him over 22 years of leadership experience across fintech, payments, credit ratings "
    "and retail banking. His most recent role was that of the Chief Business Officer at BankBazaar.com, where "
    "he has been leading the business and account management charter for the aggregator platform. Earlier, he "
    "held leadership roles at CRISIL and Mastercard, and has also worked with Citibank, HDFC Bank and ICICI "
    "Bank. His experience spans business building, distribution, partnerships, regulated businesses, financial "
    "services and large team leadership. He is an MBA from Birla Institute of Management Technology and a "
    "B.Com graduate from Jaipur Commerce College.\n\n"
    "Many of you will work closely with Pankaj in the coming days. I request each one of you to extend him "
    "your full support as he gets familiar with the organisation, our people, our strengths, our challenges "
    "and our aspirations. I am confident that under his leadership, Acuite will move into its next phase of "
    "growth and institution building.\n\n"
    "As you are aware, I will be stepping down from the position of MD & CEO at the close of July 14, 2026. "
    "That day will mark exactly 12 years since I took charge as CEO of Acuite. In the ancient Indian system "
    "of measuring time, 12 years is sometimes seen as a \"Yuga\" - a complete cycle. For me, these 12 years "
    "have indeed been a full and deeply meaningful cycle of building, learning, striving and growing together "
    "with all of you.\n\n"
    "As I am getting older and have to prioritise family and personal commitments, it was very important for "
    "me to ensure a smooth transition to the most capable successor. I am happy that our Board found a very "
    "accomplished professional for the role. I wish Pankaj a great time as part of the Acuite family.\n\n"
    "I want to thank every member of the Acuite family for your commitment, resilience, hard work and trust. "
    "Whatever the organisation has achieved over these years has been because of the collective effort of its "
    "people. It has been my privilege to serve this institution and to work alongside colleagues who cared "
    "deeply about its credibility and future.\n\n"
    "Acuite has strong foundations, a meaningful purpose, and a significant opportunity ahead. I wish "
    "Pankaj, the leadership team, and each one of you the very best as the company begins its next chapter.\n\n"
    "Warm regards,\n"
    "Sankar Chakraborti"
)


def publish_ceo_desk_leadership_transition(apps, schema_editor):
    Post = apps.get_model("feed", "Post")
    User = apps.get_model("accounts", "User")

    existing_post = (
        Post.objects.filter(
            module="bulletin",
            topic="announcements",
            title=CEO_DESK_TITLE,
            body=CEO_DESK_BODY,
        )
        .order_by("-created_at")
        .first()
    )
    if existing_post:
        return

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

    Post.objects.create(
        author=author,
        title=CEO_DESK_TITLE,
        body=CEO_DESK_BODY,
        kind="announcement",
        module="bulletin",
        topic="announcements",
        visibility="company",
        moderation_status="published",
        allow_comments=False,
        published_at=timezone.now(),
        metadata={
            "bulletin_category": "announcements",
            "bulletin_channel": "ceo_desk",
            "bulletin_template": "ceo_editorial",
            "bulletin_meta_lines": ["29 June 2026"],
            "ceo_desk_subject_line": CEO_DESK_TITLE,
            "post_as_company": True,
            "company_author_name": "Sankar Chakraborti",
            "company_author_title": "MD & CEO",
            "company_author_initials": "SC",
        },
    )


class Migration(migrations.Migration):
    dependencies = [
        ("feed", "0026_remove_people_culture_yoga_winner_cards"),
    ]

    operations = [
        migrations.RunPython(
            publish_ceo_desk_leadership_transition,
            migrations.RunPython.noop,
        ),
    ]
