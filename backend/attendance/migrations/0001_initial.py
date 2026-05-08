from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="AttendanceDayRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("attendance_date", models.DateField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("present", "Present"),
                            ("no_punchout", "No Punchout"),
                            ("not_marked", "Not Marked"),
                            ("not_applicable", "Not Applicable"),
                            ("holiday", "Holiday"),
                            ("weekend", "Weekend"),
                        ],
                        default="not_marked",
                        max_length=24,
                    ),
                ),
                ("punch_in_at", models.DateTimeField(blank=True, null=True)),
                ("punch_out_at", models.DateTimeField(blank=True, null=True)),
                ("first_activity_at", models.DateTimeField(blank=True, null=True)),
                ("last_activity_at", models.DateTimeField(blank=True, null=True)),
                ("office_label", models.CharField(blank=True, max_length=120)),
                ("punch_in_ip", models.GenericIPAddressField(blank=True, null=True)),
                ("last_activity_ip", models.GenericIPAddressField(blank=True, null=True)),
                (
                    "punch_in_source",
                    models.CharField(
                        choices=[("activity", "Connect activity"), ("logout", "Logout"), ("system", "System")],
                        default="activity",
                        max_length=24,
                    ),
                ),
                (
                    "punch_out_source",
                    models.CharField(
                        blank=True,
                        choices=[("activity", "Connect activity"), ("logout", "Logout"), ("system", "System")],
                        max_length=24,
                    ),
                ),
                ("requires_regularization", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attendance_day_records",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-attendance_date", "user__first_name", "user__last_name", "user__email"),
                "permissions": [("view_attendance_admin", "Can view attendance administration")],
            },
        ),
        migrations.AddConstraint(
            model_name="attendancedayrecord",
            constraint=models.UniqueConstraint(
                fields=("user", "attendance_date"),
                name="attendance_unique_day_record_per_user",
            ),
        ),
    ]
