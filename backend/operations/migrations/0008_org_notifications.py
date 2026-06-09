from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("operations", "0007_reportederror_attachment"),
    ]

    operations = [
        migrations.CreateModel(
            name="OrgNotification",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("message", models.TextField(blank=True)),
                (
                    "category",
                    models.CharField(
                        choices=[
                            ("announcement", "Announcement"),
                            ("bulletin", "Bulletin"),
                            ("event", "Event"),
                            ("resource", "Resource"),
                            ("general", "General"),
                        ],
                        default="general",
                        max_length=32,
                    ),
                ),
                ("target_tab", models.CharField(blank=True, max_length=64)),
                ("target_url", models.CharField(blank=True, max_length=255)),
                ("metadata", models.JSONField(blank=True, default=dict)),
                ("is_active", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="created_org_notifications",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
            },
        ),
        migrations.CreateModel(
            name="OrgNotificationRead",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("read_at", models.DateTimeField(auto_now_add=True)),
                (
                    "notification",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reads",
                        to="operations.orgnotification",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="org_notification_reads",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-read_at",),
                "unique_together": {("notification", "user")},
            },
        ),
        migrations.AddIndex(
            model_name="orgnotification",
            index=models.Index(fields=["is_active", "-created_at"], name="operations__is_acti_54af2a_idx"),
        ),
        migrations.AddIndex(
            model_name="orgnotification",
            index=models.Index(fields=["category", "-created_at"], name="operations__categor_30b461_idx"),
        ),
        migrations.AddIndex(
            model_name="orgnotificationread",
            index=models.Index(fields=["user", "-read_at"], name="operations__user_id_ceaaa3_idx"),
        ),
    ]
