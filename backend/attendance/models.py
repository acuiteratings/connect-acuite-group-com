from django.conf import settings
from django.db import models


class AttendanceDayRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = "present", "Present"
        NO_PUNCHOUT = "no_punchout", "No Punchout"
        NOT_MARKED = "not_marked", "Not Marked"
        NOT_APPLICABLE = "not_applicable", "Not Applicable"
        HOLIDAY = "holiday", "Holiday"
        WEEKEND = "weekend", "Weekend"

    class Source(models.TextChoices):
        ACTIVITY = "activity", "Connect activity"
        LOGOUT = "logout", "Logout"
        SYSTEM = "system", "System"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="attendance_day_records",
    )
    attendance_date = models.DateField()
    status = models.CharField(
        max_length=24,
        choices=Status.choices,
        default=Status.NOT_MARKED,
    )
    punch_in_at = models.DateTimeField(blank=True, null=True)
    punch_out_at = models.DateTimeField(blank=True, null=True)
    first_activity_at = models.DateTimeField(blank=True, null=True)
    last_activity_at = models.DateTimeField(blank=True, null=True)
    office_label = models.CharField(max_length=120, blank=True)
    punch_in_ip = models.GenericIPAddressField(blank=True, null=True)
    last_activity_ip = models.GenericIPAddressField(blank=True, null=True)
    punch_in_source = models.CharField(max_length=24, choices=Source.choices, default=Source.ACTIVITY)
    punch_out_source = models.CharField(max_length=24, choices=Source.choices, blank=True)
    requires_regularization = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-attendance_date", "user__first_name", "user__last_name", "user__email")
        constraints = [
            models.UniqueConstraint(
                fields=("user", "attendance_date"),
                name="attendance_unique_day_record_per_user",
            )
        ]
        permissions = [
            ("view_attendance_admin", "Can view attendance administration"),
        ]

    def __str__(self):
        return f"{self.user.full_name} - {self.attendance_date}"
