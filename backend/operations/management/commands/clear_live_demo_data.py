from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import LoginChallenge, TrustedAppLoginGrant
from feed.models import Comment, Post
from operations.models import AnalyticsEvent, AuditLog, ErrorEvent


class Command(BaseCommand):
    help = "Remove seeded/demo operational content so Connect can begin live testing cleanly."

    @transaction.atomic
    def handle(self, *args, **options):
        deletion_counts = {
            "comments": Comment.objects.count(),
            "posts": Post.objects.count(),
            "login_challenges": LoginChallenge.objects.count(),
            "trusted_login_grants": TrustedAppLoginGrant.objects.count(),
            "analytics_events": AnalyticsEvent.objects.count(),
            "audit_logs": AuditLog.objects.count(),
            "error_events": ErrorEvent.objects.count(),
        }

        Comment.objects.all().delete()
        Post.objects.all().delete()
        LoginChallenge.objects.all().delete()
        TrustedAppLoginGrant.objects.all().delete()
        AnalyticsEvent.objects.all().delete()
        AuditLog.objects.all().delete()
        ErrorEvent.objects.all().delete()

        summary = ", ".join(f"{label}={count}" for label, count in deletion_counts.items())
        self.stdout.write(self.style.SUCCESS(f"Cleared live demo data: {summary}"))
