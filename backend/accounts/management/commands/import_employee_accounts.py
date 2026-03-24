import csv
import xml.etree.ElementTree as ET
import zipfile
from datetime import date, timedelta
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from accounts.models import User
from directory.models import DirectoryProfile
from directory.utils import map_department_for_connect


def parse_bool(value, default=False):
    if value in (None, ""):
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def split_name(full_name):
    parts = [part for part in str(full_name or "").strip().split() if part]
    if not parts:
        return "", ""
    if len(parts) == 1:
        return parts[0], ""
    return parts[0], " ".join(parts[1:])


def normalize_header(value):
    return " ".join(str(value or "").strip().lower().split())


def excel_column_index(cell_reference):
    letters = "".join(character for character in str(cell_reference or "") if character.isalpha())
    value = 0
    for character in letters:
        value = (value * 26) + (ord(character.upper()) - 64)
    return max(value - 1, 0)


def excel_serial_to_date(value):
    text = str(value or "").strip()
    if not text:
        return None
    try:
        serial = int(float(text))
    except ValueError:
        return None
    if serial <= 0:
        return None
    return date(1899, 12, 30) + timedelta(days=serial)


def clean_text(value):
    return str(value or "").strip()


def first_present(row, *keys):
    for key in keys:
        value = clean_text(row.get(key, ""))
        if value:
            return value
    return ""


def _xlsx_rows(file_path):
    ns = {
        "main": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
        "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    }

    with zipfile.ZipFile(file_path) as workbook:
        shared_strings = []
        if "xl/sharedStrings.xml" in workbook.namelist():
            root = ET.fromstring(workbook.read("xl/sharedStrings.xml"))
            for item in root.findall("main:si", ns):
                shared_strings.append(
                    "".join(node.text or "" for node in item.findall(".//main:t", ns))
                )

        workbook_root = ET.fromstring(workbook.read("xl/workbook.xml"))
        rel_root = ET.fromstring(workbook.read("xl/_rels/workbook.xml.rels"))
        rel_map = {
            rel.attrib["Id"]: rel.attrib["Target"]
            for rel in rel_root.findall("rel:Relationship", ns)
        }
        sheet = workbook_root.find("main:sheets", ns)[0]
        sheet_path = "xl/" + rel_map[
            sheet.attrib["{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"]
        ]
        sheet_root = ET.fromstring(workbook.read(sheet_path))

        def cell_value(cell):
            cell_type = cell.attrib.get("t")
            raw_value = cell.find("main:v", ns)
            if cell_type == "inlineStr":
                return "".join(node.text or "" for node in cell.findall(".//main:t", ns))
            if raw_value is None:
                return ""
            raw = raw_value.text or ""
            if cell_type == "s":
                return shared_strings[int(raw)]
            return raw

        rows = []
        for row in sheet_root.findall(".//main:sheetData/main:row", ns):
            row_map = {}
            for cell in row.findall("main:c", ns):
                row_map[excel_column_index(cell.attrib.get("r", "A1"))] = cell_value(cell).strip()
            rows.append(row_map)
        return rows


def load_rows(file_path):
    path = Path(file_path)
    if path.suffix.lower() == ".csv":
        with open(path, newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            if not reader.fieldnames or "email" not in [
                field.strip().lower() for field in reader.fieldnames
            ]:
                raise CommandError("CSV must include an 'email' column.")
            return list(reader)

    if path.suffix.lower() == ".xlsx":
        rows = _xlsx_rows(path)
        if not rows:
            return []
        header_map = rows[0]
        max_column = max(header_map) if header_map else -1
        headers = [normalize_header(header_map.get(index, "")) for index in range(max_column + 1)]
        if headers[:3] != ["company name", "emp code", "user name"] and headers[:3] != [
            "company name",
            "user name",
            "email id",
        ]:
            raise CommandError(
                "XLSX must include the expected employee headers beginning with Company Name."
            )

        results = []
        for row in rows[1:]:
            normalized_row = {
                headers[index]: row.get(index, "")
                for index in range(max_column + 1)
                if headers[index]
            }
            if not any(clean_text(value) for value in normalized_row.values()):
                continue
            company_name = first_present(normalized_row, "company name")
            user_name = first_present(normalized_row, "user name")
            email = first_present(normalized_row, "email id", "email")
            first_name, last_name = split_name(user_name)
            results.append(
                {
                    "email": email,
                    "display_name": user_name,
                    "first_name": first_name,
                    "last_name": last_name,
                    "company_name": company_name,
                    "employee_code": first_present(normalized_row, "emp code", "employee code"),
                    "gender": first_present(normalized_row, "gender"),
                    "date_of_birth": excel_serial_to_date(
                        first_present(normalized_row, "date of birth")
                    ),
                    "phone_number": first_present(
                        normalized_row,
                        "mobile no",
                        "mobile number",
                        "phone number",
                    ),
                    "mobile_number": first_present(
                        normalized_row,
                        "mobile no",
                        "mobile number",
                        "phone number",
                    ),
                    "title": first_present(normalized_row, "designation", "title"),
                    "function_name": first_present(normalized_row, "function"),
                    "department": first_present(normalized_row, "department") or company_name,
                    "location": first_present(normalized_row, "office", "location"),
                    "office_location": first_present(normalized_row, "office", "location"),
                    "joined_on": excel_serial_to_date(
                        first_present(normalized_row, "date of joining", "joined on")
                    ),
                    "emergency_contact_number": first_present(
                        normalized_row,
                        "emergency contact no",
                        "emergency contact number",
                    ),
                }
            )
        return results

    raise CommandError("Only .csv and .xlsx files are supported for employee imports.")


class Command(BaseCommand):
    help = "Import employee accounts from a CSV or XLSX file for Acuite Connect."

    def add_arguments(self, parser):
        parser.add_argument("file_path", help="Absolute or relative path to the employee CSV or XLSX file.")
        parser.add_argument(
            "--temporary-password",
            default="",
            help="Optional temporary password to assign to imported users without one in the CSV.",
        )
        parser.add_argument(
            "--exclude-email",
            action="append",
            default=[],
            help="Email address to skip during import. Can be passed more than once.",
        )
        parser.add_argument(
            "--deactivate-missing",
            action="store_true",
            help="Deactivate imported-app users that are missing from this CSV.",
        )

    def handle(self, *args, **options):
        file_path = options["file_path"]
        temporary_password = str(options["temporary_password"] or "")
        excluded_emails = {
            str(email or "").strip().lower()
            for email in options["exclude_email"]
            if str(email or "").strip()
        }
        imported_emails = set()
        created = 0
        updated = 0
        skipped = 0

        try:
            rows = load_rows(file_path)
        except OSError as exc:
            raise CommandError(f"Could not open import file: {exc}") from exc

        for row_number, row in enumerate(rows, start=2):
            email = str(row.get("email", "")).strip().lower()
            if not email:
                raise CommandError(f"Row {row_number}: email is required.")
            if email in excluded_emails:
                skipped += 1
                continue

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
            DirectoryProfile.objects.update_or_create(
                user=user,
                defaults={
                    "company_name": str(row.get("company_name", "")).strip(),
                    "gender": str(row.get("gender", "")).strip(),
                    "date_of_birth": row.get("date_of_birth"),
                    "function_name": str(row.get("function_name", "")).strip(),
                    "department_for_connect": map_department_for_connect(
                        str(row.get("department", "")).strip()
                    ),
                    "city": str(row.get("location", "")).strip(),
                    "office_location": str(row.get("office_location", row.get("location", ""))).strip(),
                    "mobile_number": str(row.get("mobile_number", row.get("phone_number", ""))).strip(),
                    "emergency_contact_number": str(
                        row.get("emergency_contact_number", "")
                    ).strip(),
                    "joined_on": row.get("joined_on"),
                    "is_visible": True,
                },
            )

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
                f"Imported employees complete. Created: {created}, updated: {updated}, skipped: {skipped}, deactivated: {deactivated}."
            )
        )
