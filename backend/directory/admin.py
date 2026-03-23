from django.contrib import admin

from .models import DirectoryProfile


@admin.register(DirectoryProfile)
class DirectoryProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "manager",
        "office_location",
        "city",
        "work_mode",
        "is_visible",
        "updated_at",
    )
    list_filter = ("work_mode", "is_visible", "office_location", "city")
    search_fields = (
        "user__email",
        "user__first_name",
        "user__last_name",
        "user__display_name",
        "expertise",
        "skills",
    )
    autocomplete_fields = ("user", "manager")

# Register your models here.
