from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PeopleSyncRun",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("sync_type", models.CharField(choices=[("full", "Full"), ("incremental", "Incremental")], max_length=20)),
                ("status", models.CharField(choices=[("running", "Running"), ("success", "Success"), ("partial_success", "Partial success"), ("failed", "Failed")], default="running", max_length=24)),
                ("started_at", models.DateTimeField()),
                ("finished_at", models.DateTimeField(blank=True, null=True)),
                ("requested_updated_since", models.DateTimeField(blank=True, null=True)),
                ("next_updated_since", models.DateTimeField(blank=True, null=True)),
                ("source_generated_at", models.DateTimeField(blank=True, null=True)),
                ("records_seen", models.PositiveIntegerField(default=0)),
                ("records_created", models.PositiveIntegerField(default=0)),
                ("records_updated", models.PositiveIntegerField(default=0)),
                ("records_skipped", models.PositiveIntegerField(default=0)),
                ("records_failed", models.PositiveIntegerField(default=0)),
                ("error_summary", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ("-started_at",)},
        ),
        migrations.CreateModel(
            name="PeopleSyncFailure",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("employee_id", models.CharField(blank=True, max_length=64)),
                ("email", models.EmailField(blank=True, max_length=254)),
                ("error_code", models.CharField(blank=True, max_length=64)),
                ("error_message", models.TextField()),
                ("payload_snapshot", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("sync_run", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="failures", to="people_sync.peoplesyncrun")),
            ],
            options={"ordering": ("created_at",)},
        ),
    ]

