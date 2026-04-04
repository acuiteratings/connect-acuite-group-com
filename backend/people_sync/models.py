from django.db import models


class PeopleSyncRun(models.Model):
    class SyncType(models.TextChoices):
        FULL = "full", "Full"
        INCREMENTAL = "incremental", "Incremental"

    class Status(models.TextChoices):
        RUNNING = "running", "Running"
        SUCCESS = "success", "Success"
        PARTIAL_SUCCESS = "partial_success", "Partial success"
        FAILED = "failed", "Failed"

    sync_type = models.CharField(max_length=20, choices=SyncType.choices)
    status = models.CharField(
        max_length=24,
        choices=Status.choices,
        default=Status.RUNNING,
    )
    started_at = models.DateTimeField()
    finished_at = models.DateTimeField(blank=True, null=True)
    requested_updated_since = models.DateTimeField(blank=True, null=True)
    next_updated_since = models.DateTimeField(blank=True, null=True)
    source_generated_at = models.DateTimeField(blank=True, null=True)
    records_seen = models.PositiveIntegerField(default=0)
    records_created = models.PositiveIntegerField(default=0)
    records_updated = models.PositiveIntegerField(default=0)
    records_skipped = models.PositiveIntegerField(default=0)
    records_failed = models.PositiveIntegerField(default=0)
    error_summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-started_at",)

    def __str__(self):
        return f"{self.sync_type} sync at {self.started_at:%Y-%m-%d %H:%M:%S}"


class PeopleSyncFailure(models.Model):
    sync_run = models.ForeignKey(
        PeopleSyncRun,
        on_delete=models.CASCADE,
        related_name="failures",
    )
    employee_id = models.CharField(max_length=64, blank=True)
    email = models.EmailField(blank=True)
    error_code = models.CharField(max_length=64, blank=True)
    error_message = models.TextField()
    payload_snapshot = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return self.employee_id or self.email or "unknown employee"

