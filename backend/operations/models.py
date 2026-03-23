from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models


class AuditLog(models.Model):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="audit_logs",
        blank=True,
        null=True,
    )
    action = models.CharField(max_length=64)
    summary = models.CharField(max_length=255)
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    target_object_id = models.CharField(max_length=64, blank=True)
    request_id = models.CharField(max_length=64, blank=True, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.action} at {self.created_at:%Y-%m-%d %H:%M:%S}"


class AnalyticsEvent(models.Model):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="analytics_events",
        blank=True,
        null=True,
    )
    category = models.CharField(max_length=64)
    event_name = models.CharField(max_length=128)
    request_id = models.CharField(max_length=64, blank=True, db_index=True)
    path = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    occurred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-occurred_at",)

    def __str__(self):
        return f"{self.category}:{self.event_name}"


class ErrorEvent(models.Model):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="error_events",
        blank=True,
        null=True,
    )
    request_id = models.CharField(max_length=64, blank=True, db_index=True)
    path = models.CharField(max_length=255, blank=True)
    method = models.CharField(max_length=16, blank=True)
    status_code = models.PositiveSmallIntegerField(blank=True, null=True)
    exception_type = models.CharField(max_length=128)
    message = models.TextField()
    traceback = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(blank=True, null=True)
    occurred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-occurred_at",)

    def __str__(self):
        return f"{self.exception_type} at {self.occurred_at:%Y-%m-%d %H:%M:%S}"


class BuildState(models.Model):
    singleton_key = models.CharField(max_length=32, unique=True, default="primary")
    counter = models.PositiveIntegerField(default=1)
    display_number = models.CharField(max_length=32, default="1.0000001")
    commit_sha = models.CharField(max_length=64, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Build state"
        verbose_name_plural = "Build state"

    def __str__(self):
        return self.display_number
