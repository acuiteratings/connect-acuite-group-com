from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("operations", "0006_reportederror_resolution_notice"),
    ]

    operations = [
        migrations.AddField(
            model_name="reportederror",
            name="attachment_name",
            field=models.CharField(blank=True, max_length=180),
        ),
        migrations.AddField(
            model_name="reportederror",
            name="attachment_content_type",
            field=models.CharField(blank=True, max_length=64),
        ),
        migrations.AddField(
            model_name="reportederror",
            name="attachment_size",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="reportederror",
            name="attachment_data_url",
            field=models.TextField(blank=True),
        ),
    ]
