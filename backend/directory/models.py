from django.conf import settings
from django.db import models

from .utils import map_department_for_connect


class DirectoryProfile(models.Model):
    class WorkMode(models.TextChoices):
        ONSITE = "onsite", "On-site"
        HYBRID = "hybrid", "Hybrid"
        REMOTE = "remote", "Remote"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="directory_profile",
    )
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="direct_reports",
        blank=True,
        null=True,
    )
    company_name = models.CharField(max_length=120, blank=True)
    gender = models.CharField(max_length=32, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    function_name = models.CharField(max_length=150, blank=True)
    department_for_connect = models.CharField(max_length=120, blank=True)
    city = models.CharField(max_length=120, blank=True)
    office_location = models.CharField(max_length=120, blank=True)
    work_mode = models.CharField(
        max_length=16,
        choices=WorkMode.choices,
        default=WorkMode.HYBRID,
    )
    phone_extension = models.CharField(max_length=16, blank=True)
    mobile_number = models.CharField(max_length=32, blank=True)
    emergency_contact_number = models.CharField(max_length=32, blank=True)
    bio = models.TextField(blank=True)
    expertise = models.CharField(max_length=255, blank=True)
    skills = models.JSONField(default=list, blank=True)
    hobbies = models.JSONField(default=list, blank=True)
    interests = models.JSONField(default=list, blank=True)
    profile_photos = models.JSONField(default=list, blank=True)
    joined_on = models.DateField(blank=True, null=True)
    is_visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("user__first_name", "user__last_name", "user__email")
        permissions = [
            ("manage_directory", "Can manage employee directory records"),
        ]

    def __str__(self):
        return f"Directory profile for {self.user.full_name}"

    def save(self, *args, **kwargs):
        if self.user_id:
            self.department_for_connect = map_department_for_connect(
                getattr(self.user, "department", "")
            )
        super().save(*args, **kwargs)
