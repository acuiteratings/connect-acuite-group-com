from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("directory", "0006_communitymembership"),
    ]

    operations = [
        migrations.AddField(
            model_name="directoryprofile",
            name="attendance_recording_method",
            field=models.CharField(blank=True, max_length=120),
        ),
    ]
