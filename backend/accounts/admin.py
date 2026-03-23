from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ("email",)
    list_display = (
        "email",
        "full_name",
        "department",
        "title",
        "employment_status",
        "access_level",
        "is_staff",
    )
    list_filter = ("employment_status", "access_level", "department", "is_staff")
    search_fields = ("email", "first_name", "last_name", "display_name", "employee_code")
    readonly_fields = ("date_joined", "updated_at", "last_login", "last_seen_at")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Profile",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "display_name",
                    "employee_code",
                    "title",
                    "department",
                    "location",
                    "phone_number",
                )
            },
        ),
        (
            "Access",
            {
                "fields": (
                    "employment_status",
                    "access_level",
                    "is_directory_visible",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Lifecycle",
            {"fields": ("last_seen_at", "last_login", "date_joined", "updated_at")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "first_name",
                    "last_name",
                    "display_name",
                    "department",
                    "title",
                    "employment_status",
                    "access_level",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

# Register your models here.
