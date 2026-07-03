from django.db import migrations
from django.utils import timezone


def activate_people_synced_pending_users(apps, schema_editor):
    User = apps.get_model("accounts", "User")
    User.objects.filter(
        employment_status="pending",
        is_active=True,
        employee_code__gt="",
        directory_profile__isnull=False,
    ).update(
        employment_status="active",
        updated_at=timezone.now(),
    )


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0006_employeessoidentitysnapshot"),
        ("directory", "0007_directoryprofile_attendance_recording_method"),
        ("people_sync", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            activate_people_synced_pending_users,
            migrations.RunPython.noop,
        ),
    ]
