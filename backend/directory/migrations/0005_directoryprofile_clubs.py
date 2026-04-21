from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("directory", "0004_profile_builder_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="directoryprofile",
            name="clubs",
            field=models.JSONField(blank=True, default=list),
        ),
    ]
