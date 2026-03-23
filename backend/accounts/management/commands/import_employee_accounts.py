import csv

from django.core.management.base import BaseCommand, CommandError

from accounts.models import User


def parse_bool(value, default=False):
    if value in (None, ""):
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


class Command(BaseCommand):
    help = "Import employee accounts from a CSV file for Acuite Connect."

    def add_arguments(self, parser):
        parser.add_argument("csv_path", help="Absolute or relative path to the employee CSV file.")
        parser.add_argument(
            "--temporary-password",
            default="",
            help="Optional temporary password to assign to imported users without one in the CSV.",
        )
        parser.add_argument(
            "--deactivate-missing",
            action="store_true",
            help="Deactivate imported-app users that are missing from this CSV.",
        )

    def handle(self, *args, **options):
        csv_path = options["csv_path"]
        temporary_password = str(options["temporary_password"] or "")
        imported_emails = set()
        created = 0
        updated = 0

        try:
            csv_file = open(csv_path, newline="", encoding="utf-8-sig")
        except OSError as exc:
            raise CommandError(f"Could not open CSV file: {exc}") from exc

        with csv_file:
            reader = csv.DictReader(csv_file)
            if not reader.fieldnames or "email" not in [field.strip().lower() for field in reader.fieldnames]:
                raise CommandError("CSV must include an 'email' column.")

            for row_number, row in enumerate(reader, start=2):
                email = str(row.get("email", "")).strip().lower()
                if not email:
                    raise CommandError(f"Row {row_number}: email is required.")

                imported_emails.add(email)
                defaults = {
                    "first_name": str(row.get("first_name", "")).strip(),
                    "last_name": str(row.get("last_name", "")).strip(),
                    "display_name": str(row.get("display_name", "")).strip(),
                    "employee_code": str(row.get("employee_code", "")).strip(),
                    "title": str(row.get("title", "")).strip(),
                    "department": str(row.get("department", "")).strip(),
                    "location": str(row.get("location", "")).strip(),
                    "phone_number": str(row.get("phone_number", "")).strip(),
                    "employment_status": str(
                        row.get("employment_status", User.EmploymentStatus.ACTIVE)
                    ).strip()
                    or User.EmploymentStatus.ACTIVE,
                    "access_level": str(
                        row.get("access_level", User.AccessLevel.EMPLOYEE)
                    ).strip()
                    or User.AccessLevel.EMPLOYEE,
                    "is_staff": parse_bool(row.get("is_staff"), False),
                    "is_active": parse_bool(row.get("is_active"), True),
                    "is_directory_visible": parse_bool(row.get("is_directory_visible"), True),
                    "must_change_password": True,
                }
                user, created_now = User.objects.update_or_create(
                    email=email,
                    defaults=defaults,
                )

                row_password = str(row.get("temporary_password", "")).strip()
                chosen_password = row_password or temporary_password
                if created_now:
                    created += 1
                else:
                    updated += 1

                if chosen_password:
                    user.set_password(chosen_password)
                elif not user.password:
                    user.set_unusable_password()
                user.must_change_password = True
                user.password_changed_at = None
                user.save(update_fields=["password", "must_change_password", "password_changed_at", "updated_at"])

        deactivated = 0
        if options["deactivate_missing"]:
            queryset = User.objects.filter(is_superuser=False).exclude(email__in=imported_emails)
            deactivated = queryset.update(
                is_active=False,
                employment_status=User.EmploymentStatus.ALUMNI,
                must_change_password=True,
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported employees complete. Created: {created}, updated: {updated}, deactivated: {deactivated}."
            )
        )
