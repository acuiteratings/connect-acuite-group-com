from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from operations.models import AnalyticsEvent, AuditLog, ErrorEvent, ReportedError


class Command(BaseCommand):
    help = "Prune old operational audit, analytics, and error records."

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help="Report counts without deleting records.")
        parser.add_argument("--analytics-days", type=int, default=180)
        parser.add_argument("--audit-days", type=int, default=365)
        parser.add_argument("--resolved-errors-days", type=int, default=90)
        parser.add_argument("--unresolved-errors-days", type=int, default=365)
        parser.add_argument("--resolved-reports-days", type=int, default=180)
        parser.add_argument("--unresolved-reports-days", type=int, default=365)

    def handle(self, *args, **options):
        now = timezone.now()
        dry_run = options["dry_run"]

        targets = [
            (
                "analytics_events",
                AnalyticsEvent.objects.filter(
                    occurred_at__lt=now - timedelta(days=max(options["analytics_days"], 1))
                ),
            ),
            (
                "audit_logs",
                AuditLog.objects.filter(
                    created_at__lt=now - timedelta(days=max(options["audit_days"], 1))
                ),
            ),
            (
                "resolved_error_events",
                ErrorEvent.objects.filter(is_resolved=True).filter(
                    Q(resolved_at__lt=now - timedelta(days=max(options["resolved_errors_days"], 1)))
                    | Q(
                        resolved_at__isnull=True,
                        occurred_at__lt=now - timedelta(days=max(options["resolved_errors_days"], 1)),
                    )
                ),
            ),
            (
                "old_unresolved_error_events",
                ErrorEvent.objects.filter(
                    is_resolved=False,
                    occurred_at__lt=now - timedelta(days=max(options["unresolved_errors_days"], 1)),
                ),
            ),
            (
                "resolved_reported_errors",
                ReportedError.objects.filter(is_resolved=True).filter(
                    Q(resolved_at__lt=now - timedelta(days=max(options["resolved_reports_days"], 1)))
                    | Q(
                        resolved_at__isnull=True,
                        created_at__lt=now - timedelta(days=max(options["resolved_reports_days"], 1)),
                    )
                ),
            ),
            (
                "old_unresolved_reported_errors",
                ReportedError.objects.filter(
                    is_resolved=False,
                    created_at__lt=now - timedelta(days=max(options["unresolved_reports_days"], 1)),
                ),
            ),
        ]

        pruned = {}
        for label, queryset in targets:
            count = queryset.count()
            pruned[label] = count
            if count and not dry_run:
                queryset.delete()

        action = "Would prune" if dry_run else "Pruned"
        self.stdout.write(
            self.style.SUCCESS(
                f"{action}: "
                + ", ".join(f"{label}={count}" for label, count in pruned.items())
            )
        )
