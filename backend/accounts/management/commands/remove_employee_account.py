from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from accounts.models import User
from operations.models import AnalyticsEvent, AuditLog, ErrorEvent


class Command(BaseCommand):
    help = "Remove a single employee account and related Connect data by email."

    def add_arguments(self, parser):
        parser.add_argument("email", help="Email address of the employee account to remove.")

    @transaction.atomic
    def handle(self, *args, **options):
        email = str(options["email"] or "").strip().lower()
        if not email:
            raise CommandError("An email address is required.")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as exc:
            raise CommandError(f"No employee account found for {email}.") from exc

        if user.is_staff or user.is_superuser:
            raise CommandError(
                f"Refusing to delete privileged account {email}. Remove it manually if intended."
            )

        deletion_counts = {
            "directory_profile": 1 if hasattr(user, "directory_profile") else 0,
            "posts": user.posts.count(),
            "comments": user.comments.count(),
            "login_challenges": user.login_challenges.count(),
            "trusted_login_grants": user.trusted_login_grants.count(),
            "analytics_events": AnalyticsEvent.objects.filter(actor=user).count(),
            "audit_logs": AuditLog.objects.filter(actor=user).count(),
            "error_events": ErrorEvent.objects.filter(actor=user).count(),
        }

        AnalyticsEvent.objects.filter(actor=user).delete()
        AuditLog.objects.filter(actor=user).delete()
        ErrorEvent.objects.filter(actor=user).delete()
        user.delete()

        summary = ", ".join(f"{label}={count}" for label, count in deletion_counts.items())
        self.stdout.write(
            self.style.SUCCESS(f"Removed employee account {email}. Deleted: {summary}")
        )
