from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import LoginChallenge, User


@admin.action(description="Require password change on next login")
def require_password_change(modeladmin, request, queryset):
    queryset.update(must_change_password=True)


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
        "must_change_password",
        "password_due_display",
    )
    list_filter = ("employment_status", "access_level", "department", "is_staff")
    search_fields = ("email", "first_name", "last_name", "display_name", "employee_code")
    readonly_fields = (
        "date_joined",
        "updated_at",
        "last_login",
        "last_seen_at",
        "password_changed_at",
        "password_due_display",
    )
    actions = (require_password_change,)
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
                    "must_change_password",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Password Policy",
            {"fields": ("password_changed_at", "password_due_display")},
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
                    "must_change_password",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    def password_due_display(self, obj):
        if not obj.password_due_at:
            return "Password setup pending"
        if obj.password_change_required:
            return f"Overdue since {obj.password_due_at:%Y-%m-%d}"
        return obj.password_due_at.strftime("%Y-%m-%d")

    password_due_display.short_description = "Password due"


@admin.register(LoginChallenge)
class LoginChallengeAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "purpose",
        "otp_sent_at",
        "expires_at",
        "otp_verified_at",
        "password_verified_at",
        "consumed_at",
    )
    list_filter = ("purpose", "otp_verified_at", "consumed_at")
    search_fields = ("email", "public_id", "user__email")
    readonly_fields = (
        "public_id",
        "user",
        "email",
        "purpose",
        "code_hash",
        "otp_sent_at",
        "expires_at",
        "otp_verified_at",
        "password_verified_at",
        "consumed_at",
        "otp_attempts",
        "password_attempts",
        "created_at",
        "updated_at",
    )

# Register your models here.
