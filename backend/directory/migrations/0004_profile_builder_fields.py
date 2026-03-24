from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("directory", "0003_department_for_connect"),
    ]

    operations = [
        migrations.AddField(
            model_name="directoryprofile",
            name="hobbies",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="directoryprofile",
            name="interests",
            field=models.JSONField(blank=True, default=list),
        ),
        migrations.AddField(
            model_name="directoryprofile",
            name="profile_photos",
            field=models.JSONField(blank=True, default=list),
        ),
    ]
