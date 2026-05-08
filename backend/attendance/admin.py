from django.contrib import admin

from .models import AttendanceDayRecord


@admin.register(AttendanceDayRecord)
class AttendanceDayRecordAdmin(admin.ModelAdmin):
    list_display = (
        "attendance_date",
        "user",
        "status",
        "office_label",
        "punch_in_at",
        "punch_out_at",
        "requires_regularization",
        "updated_at",
    )
    list_filter = ("status", "attendance_date", "office_label", "requires_regularization")
    search_fields = ("user__email", "user__first_name", "user__last_name", "user__display_name")
    autocomplete_fields = ("user",)
