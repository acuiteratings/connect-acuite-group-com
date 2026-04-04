from datetime import datetime, timezone as dt_timezone

from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from people_sync.services import PeopleSyncError, run_people_sync


class Command(BaseCommand):
    help = "Sync employee directory data from the People app into Connect."

    def add_arguments(self, parser):
        parser.add_argument(
            "--full",
            action="store_true",
            help="Run a full sync instead of an incremental sync.",
        )
        parser.add_argument(
            "--updated-since",
            default="",
            help="Override the incremental checkpoint with an ISO UTC timestamp.",
        )

    def handle(self, *args, **options):
        sync_type = "full" if options["full"] else "incremental"
        requested_updated_since = None
        raw_updated_since = str(options.get("updated_since") or "").strip()
        if raw_updated_since:
            normalized = raw_updated_since.replace("Z", "+00:00")
            try:
                requested_updated_since = datetime.fromisoformat(normalized)
            except ValueError as exc:
                raise CommandError("--updated-since must be a valid ISO datetime.") from exc
            if timezone.is_naive(requested_updated_since):
                requested_updated_since = timezone.make_aware(
                    requested_updated_since,
                    dt_timezone.utc,
                )
            requested_updated_since = requested_updated_since.astimezone(dt_timezone.utc)

        try:
            run = run_people_sync(
                sync_type=sync_type,
                requested_updated_since=requested_updated_since,
            )
        except PeopleSyncError as exc:
            raise CommandError(str(exc)) from exc

        if run.status == run.Status.FAILED:
            raise CommandError(run.error_summary or "People sync failed.")

        self.stdout.write(
            self.style.SUCCESS(
                f"{run.sync_type} sync finished with status={run.status}; "
                f"seen={run.records_seen}, created={run.records_created}, "
                f"updated={run.records_updated}, failed={run.records_failed}."
            )
        )
