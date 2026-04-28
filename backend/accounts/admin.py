from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import ExitProcess, LoginChallenge, User


@admin.action(description="Require password change on next login")
def require_password_change(_modeladmin, request, queryset):
    queryset.update(must_change_password=True)


@admin.action(description="Disable posting access in Connect")
def disable_connect_posting(_modeladmin, request, queryset):
    queryset.update(can_post_in_connect=False)


@admin.action(description="Restore posting access in Connect")
def restore_connect_posting(_modeladmin, request, queryset):
    queryset.update(can_post_in_connect=True)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ("email",)
    list_display = (
        "email",
        "full_name",
        "employee_code",
        "department",
        "title",
        "employment_status",
        "access_level",
        "can_post_in_connect",
        "is_staff",
        "must_change_password",
        "password_due_display",
    )
    list_filter = (
        "employment_status",
        "access_level",
        "can_post_in_connect",
        "department",
        "location",
        "is_staff",
    )
    search_fields = ("email", "first_name", "last_name", "display_name", "employee_code")
    readonly_fields = (
        "date_joined",
        "updated_at",
        "last_login",
        "last_seen_at",
        "password_changed_at",
        "password_due_display",
    )
    actions = (require_password_change, disable_connect_posting, restore_connect_posting)
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
                    "can_post_in_connect",
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
                    "can_post_in_connect",
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

@admin.register(ExitProcess)
class ExitProcessAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "stage",
        "resignation_date",
        "last_working_day",
        "resignation_acknowledged",
        "knowledge_transfer_completed",
        "assets_returned",
        "access_review_completed",
        "alumni_transition_completed",
        "completed_at",
    )
    list_filter = (
        "stage",
        "resignation_acknowledged",
        "knowledge_transfer_completed",
        "assets_returned",
        "access_review_completed",
        "alumni_transition_completed",
    )
    search_fields = (
        "employee__email",
        "employee__display_name",
        "employee__first_name",
        "employee__last_name",
        "notes",
    )
    readonly_fields = ("created_at", "updated_at", "completed_at")
