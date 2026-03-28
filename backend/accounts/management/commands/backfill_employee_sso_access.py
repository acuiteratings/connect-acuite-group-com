from django.core.management.base import BaseCommand, CommandError

from accounts.models import User


class Command(BaseCommand):
    help = (
        "One-time backfill for Employee SSO linked users so existing Connect accounts "
        "remain authorized locally after SSO login."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "emails",
            nargs="*",
            help="Optional employee email addresses to backfill. If omitted, use --all-linked.",
        )
        parser.add_argument(
            "--all-linked",
            action="store_true",
            help="Backfill every user who already has an Employee SSO identity snapshot.",
        )
        parser.add_argument(
            "--all-users",
            action="store_true",
            help="Backfill every existing Connect user, whether linked to Employee SSO yet or not.",
        )
        parser.add_argument(
            "--enable-posting",
            action="store_true",
            help="Also enable Connect posting for the selected users.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview the users that would be updated without saving changes.",
        )

    def handle(self, *args, **options):
        emails = [
            str(email or "").strip().lower()
            for email in options["emails"]
            if str(email or "").strip()
        ]
        all_linked = bool(options["all_linked"])
        all_users = bool(options["all_users"])
        enable_posting = bool(options["enable_posting"])
        dry_run = bool(options["dry_run"])

        selection_count = sum([bool(emails), all_linked, all_users])
        if selection_count > 1:
            raise CommandError("Use one selector only: email addresses, --all-linked, or --all-users.")
        if selection_count == 0:
            raise CommandError("Provide one or more email addresses, or use --all-linked / --all-users.")

        queryset = User.objects.select_related("employee_sso_identity").order_by("email")
        if all_users:
            queryset = queryset.exclude(
                employment_status__in=[
                    User.EmploymentStatus.ALUMNI,
                    User.EmploymentStatus.SUSPENDED,
                ]
            )
        elif all_linked:
            queryset = queryset.filter(employee_sso_identity__isnull=False)
        else:
            queryset = queryset.filter(email__in=emails)

        users = list(queryset)
        if not users:
            raise CommandError("No matching Employee SSO-linked users were found.")

        updated = []
        skipped = []
        for user in users:
            if all_linked and not hasattr(user, "employee_sso_identity"):
                skipped.append(f"{user.email} -> skipped (no Employee SSO link found)")
                continue

            update_fields = []
            changes = []
            if user.employment_status == User.EmploymentStatus.PENDING:
                user.employment_status = User.EmploymentStatus.ACTIVE
                update_fields.append("employment_status")
                changes.append("employment_status=active")
            if not user.is_active:
                user.is_active = True
                update_fields.append("is_active")
                changes.append("is_active=true")
            if enable_posting and not user.can_post_in_connect:
                user.can_post_in_connect = True
                update_fields.append("can_post_in_connect")
                changes.append("posting=enabled")

            if not update_fields:
                skipped.append(f"{user.email} -> skipped (already active locally)")
                continue

            if not dry_run:
                user.save(update_fields=[*update_fields, "updated_at"])
            updated.append(f"{user.email} -> {', '.join(changes)}")

        if dry_run:
            self.stdout.write(self.style.WARNING("Dry run only. No changes were saved."))

        if updated:
            self.stdout.write(self.style.SUCCESS("Backfilled Employee SSO-linked Connect access:"))
            for line in updated:
                self.stdout.write(f" - {line}")
        else:
            self.stdout.write(self.style.WARNING("No users needed backfill updates."))

        if skipped:
            self.stdout.write("Skipped:")
            for line in skipped:
                self.stdout.write(f" - {line}")
