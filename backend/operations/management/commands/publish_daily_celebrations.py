from datetime import date

from django.core.management.base import BaseCommand, CommandError

from operations.celebrations import publish_daily_celebration_posts


class Command(BaseCommand):
    help = "Publish automatic birthday and work anniversary bulletin posts for the selected date."

    def add_arguments(self, parser):
        parser.add_argument(
            "--date",
            default="",
            help="Reference date in YYYY-MM-DD format. Defaults to today in Connect timezone.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show which posts would be created without publishing them.",
        )

    def handle(self, *args, **options):
        raw_date = str(options["date"] or "").strip()
        reference_date = None
        if raw_date:
            try:
                reference_date = date.fromisoformat(raw_date)
            except ValueError as exc:
                raise CommandError("Date must be in YYYY-MM-DD format.") from exc

        result = publish_daily_celebration_posts(
            reference_date=reference_date,
            dry_run=bool(options["dry_run"]),
        )
        created = result["created"]
        skipped = result["skipped_existing"]
        mode_label = "Would create" if options["dry_run"] else "Created"
        self.stdout.write(
            f"{mode_label} {len(created)} celebration post(s) for {result['reference_date']}."
        )
        for item in created:
            self.stdout.write(
                f"- {item['template_key']}: {item['title']} ({item['employee_email']})"
            )
        if skipped:
            self.stdout.write(f"Skipped {len(skipped)} existing post(s).")
