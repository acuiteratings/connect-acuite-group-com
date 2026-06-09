from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("operations", "0005_reportederror_resolution"),
    ]

    operations = [
        migrations.AddField(
            model_name="reportederror",
            name="resolution_outcome",
            field=models.CharField(
                blank=True,
                choices=[
                    ("resolved", "Resolved"),
                    ("not_an_error", "Not an error"),
                ],
                max_length=24,
            ),
        ),
        migrations.AddField(
            model_name="reportederror",
            name="resolution_comment",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="reportederror",
            name="reporter_seen_at",
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RunSQL(
            "UPDATE operations_reportederror SET resolution_outcome = 'resolved' WHERE is_resolved = TRUE AND resolution_outcome = ''",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
