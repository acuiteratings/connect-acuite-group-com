from django.db import migrations


ANNOUNCEMENT_LINK = "https://forms.office.com/r/DvZ2mHS27t"
ANNOUNCEMENT_BODY = (
    "Take this quick 10-minute assessment using the link below to evaluate your "
    "cybersecurity awareness. Participation is mandatory for all employees. "
    f"Link: {ANNOUNCEMENT_LINK}"
)
ANNOUNCEMENT_WHEN = "Last Date - June 2, 2026"
ANNOUNCEMENT_DATE_LABEL = "June 2, 2026"


def extend_cybersecurity_deadline(apps, schema_editor):
    Post = apps.get_model("feed", "Post")

    for post in Post.objects.filter(module="bulletin", topic="announcements").order_by("-created_at"):
        metadata = dict(post.metadata or {})
        tag = str(metadata.get("home_announcement_tag", "")).strip().lower()
        if tag != "cybersecurity":
            continue

        metadata["bulletin_meta_lines"] = [ANNOUNCEMENT_WHEN]
        display = dict(metadata.get("home_announcement_display") or {})
        display.update(
            {
                "dateLabel": ANNOUNCEMENT_DATE_LABEL,
                "timeLabel": "Last Date",
                "summary": ANNOUNCEMENT_BODY,
                "ctaLabel": "Open assessment",
                "ctaTarget": ANNOUNCEMENT_LINK,
            }
        )
        metadata["home_announcement_display"] = display
        metadata["bulletin_cta_label"] = "Open assessment"
        metadata["bulletin_cta_target"] = ANNOUNCEMENT_LINK

        post.body = ANNOUNCEMENT_BODY
        post.metadata = metadata
        post.save(update_fields=["body", "metadata", "updated_at"])
        break


class Migration(migrations.Migration):
    dependencies = [
        ("feed", "0014_update_cybersecurity_assessment_announcement"),
    ]

    operations = [
        migrations.RunPython(
            extend_cybersecurity_deadline,
            migrations.RunPython.noop,
        ),
    ]
