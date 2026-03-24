from django.contrib import admin

from .models import DirectoryProfile


@admin.register(DirectoryProfile)
class DirectoryProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "company_name",
        "department_for_connect",
        "function_name",
        "manager",
        "office_location",
        "city",
        "work_mode",
        "is_visible",
        "updated_at",
    )
    list_filter = (
        "company_name",
        "department_for_connect",
        "function_name",
        "work_mode",
        "is_visible",
        "office_location",
        "city",
    )
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "user__display_name",
        "company_name",
        "department_for_connect",
        "function_name",
        "expertise",
        "skills",
    )
    autocomplete_fields = ("user", "manager")
