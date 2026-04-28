from django.utils import timezone

from django.contrib import admin

from .models import AnalyticsEvent, AuditLog, ErrorEvent, ReportedError


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "action", "actor", "summary", "request_id", "ip_address")
    list_filter = ("action", "created_at")
    search_fields = ("summary", "actor__email", "target_object_id", "request_id")
    readonly_fields = (
        "actor",
        "action",
        "summary",
        "target_content_type",
        "target_object_id",
        "request_id",
        "metadata",
        "ip_address",
        "user_agent",
        "created_at",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AnalyticsEvent)
class AnalyticsEventAdmin(admin.ModelAdmin):
    list_display = ("occurred_at", "category", "event_name", "actor", "request_id", "path")
    list_filter = ("category", "occurred_at")
    search_fields = ("event_name", "actor__email", "path", "request_id")
    readonly_fields = (
        "actor",
        "category",
        "event_name",
        "request_id",
        "path",
        "metadata",
        "ip_address",
        "user_agent",
        "occurred_at",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.action(description="Mark selected errors as resolved")
def mark_errors_resolved(_modeladmin, request, queryset):
    queryset.update(is_resolved=True, resolved_at=timezone.now())


@admin.register(ErrorEvent)
class ErrorEventAdmin(admin.ModelAdmin):
    list_display = (
        "occurred_at",
        "exception_type",
        "path",
        "status_code",
        "request_id",
        "is_resolved",
    )
    list_filter = ("exception_type", "status_code", "is_resolved", "occurred_at")
    search_fields = ("message", "path", "request_id", "actor__email")
    readonly_fields = (
        "actor",
        "request_id",
        "path",
        "method",
        "status_code",
        "exception_type",
        "message",
        "traceback",
        "metadata",
        "ip_address",
        "user_agent",
        "occurred_at",
        "resolved_at",
    )
    actions = (mark_errors_resolved,)

    def has_add_permission(self, request):
        return False


@admin.action(description="Mark selected reported errors as resolved")
def mark_reported_errors_resolved(_modeladmin, request, queryset):
    queryset.filter(is_resolved=False).update(
        is_resolved=True,
        resolved_at=timezone.now(),
        resolved_by=request.user,
    )


@admin.register(ReportedError)
class ReportedErrorAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "title",
        "reporter",
        "source_tab",
        "page_path",
        "is_resolved",
        "resolved_at",
    )
    list_filter = ("is_resolved", "source_tab", "created_at")
    search_fields = ("title", "details", "reporter__email", "reporter__first_name", "reporter__last_name")
    readonly_fields = (
        "reporter",
        "title",
        "details",
        "source_tab",
        "page_path",
        "metadata",
        "created_at",
        "resolved_at",
        "resolved_by",
    )
    actions = (mark_reported_errors_resolved,)

    def has_add_permission(self, request):
        return False
