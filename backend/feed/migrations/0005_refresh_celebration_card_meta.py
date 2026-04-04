from django.db import migrations


def refresh_celebration_card_meta(apps, schema_editor):
    Post = apps.get_model("feed", "Post")
    DirectoryProfile = apps.get_model("directory", "DirectoryProfile")

    celebration_keys = {"birthday_wish", "work_anniversary"}

    profiles = {
        profile.user_id: profile
        for profile in DirectoryProfile.objects.select_related("user").all()
    }

    for post in Post.objects.filter(module="bulletin").iterator():
        metadata = dict(post.metadata or {})
        template_key = str(
            metadata.get("bulletin_auto_kind")
            or metadata.get("bulletin_template")
            or ""
        ).strip()
        if template_key not in celebration_keys:
            continue

        card = metadata.get("bulletin_card")
        if not isinstance(card, dict):
            continue

        employee_user_id = metadata.get("bulletin_employee_user_id")
        profile = profiles.get(employee_user_id)
        if not profile:
            continue

        location = str(
            getattr(profile, "office_location", "")
            or getattr(profile, "city", "")
            or getattr(profile.user, "location", "")
            or ""
        ).strip()
        department = str(
            getattr(profile, "department_for_connect", "")
            or getattr(profile.user, "department", "")
            or getattr(profile, "company_name", "")
            or ""
        ).strip()
        person_role = " | ".join(part for part in [location, department] if part)

        if card.get("person_role") == person_role:
            continue

        card["person_role"] = person_role
        metadata["bulletin_card"] = card
        post.metadata = metadata
        post.save(update_fields=["metadata", "updated_at"])


class Migration(migrations.Migration):
    dependencies = [
        ("directory", "0003_department_for_connect"),
        ("feed", "0004_narrow_post_modules"),
    ]

    operations = [
        migrations.RunPython(refresh_celebration_card_meta, migrations.RunPython.noop),
    ]
