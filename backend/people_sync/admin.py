from django.contrib import admin

from .models import PeopleSyncFailure, PeopleSyncRun


@admin.register(PeopleSyncRun)
class PeopleSyncRunAdmin(admin.ModelAdmin):
    list_display = (
        "sync_type",
        "status",
        "started_at",
        "finished_at",
        "records_seen",
        "records_created",
        "records_updated",
        "records_failed",
    )
    list_filter = ("sync_type", "status", "started_at")
    readonly_fields = (
        "sync_type",
        "status",
        "started_at",
        "finished_at",
        "requested_updated_since",
        "next_updated_since",
        "source_generated_at",
        "records_seen",
        "records_created",
        "records_updated",
        "records_skipped",
        "records_failed",
        "error_summary",
        "created_at",
    )


@admin.register(PeopleSyncFailure)
class PeopleSyncFailureAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "email", "error_code", "created_at")
    list_filter = ("error_code", "created_at")
    search_fields = ("employee_id", "email", "error_message")
    readonly_fields = (
        "sync_run",
        "employee_id",
        "email",
        "error_code",
        "error_message",
        "payload_snapshot",
        "created_at",
    )

