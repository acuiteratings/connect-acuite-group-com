import json
from datetime import date, datetime, timezone as dt_timezone
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from accounts.models import User
from directory.models import DirectoryProfile
from directory.utils import map_department_for_connect

from .models import PeopleSyncFailure, PeopleSyncRun


class PeopleSyncError(RuntimeError):
    pass


def _isoformat_utc(value):
    if value is None:
        return ""
    if timezone.is_naive(value):
        value = timezone.make_aware(value, timezone.get_current_timezone())
    value = value.astimezone(dt_timezone.utc)
    return value.replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _ensure_https_people_api_url(url):
    parsed = urlparse(str(url or "").strip())
    if parsed.scheme == "https" and parsed.netloc:
        return
    if (
        getattr(settings, "DEBUG", False)
        and parsed.scheme == "http"
        and parsed.hostname in {"127.0.0.1", "localhost"}
    ):
        return
    raise PeopleSyncError("People API URL must be HTTPS.")


def _parse_iso_datetime(value, field_name):
    raw_value = str(value or "").strip()
    if not raw_value:
        raise ValueError(f"{field_name} is required.")
    normalized = raw_value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a valid ISO datetime.") from exc
    if timezone.is_naive(parsed):
        parsed = timezone.make_aware(parsed, dt_timezone.utc)
    return parsed.astimezone(dt_timezone.utc)


def _parse_optional_date(value):
    raw_value = str(value or "").strip()
    if not raw_value:
        return None
    return date.fromisoformat(raw_value)


def _split_name_parts(item):
    display_name = str(
        item.get("display_name")
        or item.get("full_name")
        or item.get("email", "").split("@", 1)[0].replace(".", " ").replace("_", " ").title()
    ).strip()
    first_name = str(item.get("first_name") or "").strip()
    last_name = str(item.get("last_name") or "").strip()
    if first_name or last_name:
        return display_name, first_name, last_name
    parts = [part for part in display_name.split() if part]
    if not parts:
        return "", "", ""
    if len(parts) == 1:
        return display_name, parts[0], ""
    return display_name, parts[0], " ".join(parts[1:])


def _validate_employee_item(item):
    payload = dict(item or {})
    required_fields = [
        "employee_id",
        "email",
        "full_name",
        "employment_status",
        "is_directory_visible",
        "source_updated_at",
    ]
    missing = [field for field in required_fields if not str(payload.get(field, "")).strip() and field != "is_directory_visible"]
    if "is_directory_visible" not in payload:
        missing.append("is_directory_visible")
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(sorted(set(missing)))}.")
    payload["employee_id"] = str(payload.get("employee_id") or "").strip()
    payload["email"] = str(payload.get("email") or "").strip().lower()
    payload["full_name"] = str(payload.get("full_name") or "").strip()
    payload["source_updated_at"] = _parse_iso_datetime(
        payload.get("source_updated_at"),
        "source_updated_at",
    )
    payload["is_directory_visible"] = bool(payload.get("is_directory_visible"))
    return payload


def _map_employment_status(value):
    normalized = str(value or "").strip().lower()
    if normalized in {"alumni", "exited", "exit"}:
        return User.EmploymentStatus.ALUMNI
    if normalized == "suspended":
        return User.EmploymentStatus.SUSPENDED
    if normalized == "pending":
        return User.EmploymentStatus.PENDING
    return User.EmploymentStatus.ACTIVE


def _resolve_local_employment_status(existing_user, source_status):
    if source_status in {User.EmploymentStatus.ALUMNI, User.EmploymentStatus.SUSPENDED}:
        return source_status
    if existing_user and existing_user.employment_status == User.EmploymentStatus.PENDING:
        return User.EmploymentStatus.PENDING
    return User.EmploymentStatus.ACTIVE


def _directory_visibility_for_source(source_status, requested_visibility):
    return bool(requested_visibility) and source_status == User.EmploymentStatus.ACTIVE


def _find_user_for_sync(employee_id, email):
    employee_id = str(employee_id or "").strip()
    email = str(email or "").strip().lower()
    if employee_id:
        user = User.objects.filter(employee_code=employee_id).order_by("id").first()
        if user:
            return user
    if email:
        return User.objects.filter(email=email).order_by("id").first()
    return None


def _apply_user_fields(user, item, *, source_status, is_new):
    display_name, first_name, last_name = _split_name_parts(item)
    resolved_status = (
        User.EmploymentStatus.PENDING
        if is_new and source_status == User.EmploymentStatus.ACTIVE
        else _resolve_local_employment_status(None if is_new else user, source_status)
    )
    source_visible = _directory_visibility_for_source(
        source_status,
        item.get("is_directory_visible"),
    )
    desired_values = {
        "email": item["email"],
        "first_name": first_name,
        "last_name": last_name,
        "display_name": display_name,
        "employee_code": item["employee_id"],
        "title": str(item.get("title") or "").strip(),
        "department": str(item.get("department") or "").strip(),
        "location": str(item.get("office_location") or item.get("city") or "").strip(),
        "phone_number": str(item.get("mobile_number") or "").strip(),
        "employment_status": resolved_status,
        "is_directory_visible": source_visible,
        "is_active": source_status != User.EmploymentStatus.ALUMNI,
    }

    update_fields = []
    for field_name, desired_value in desired_values.items():
        if getattr(user, field_name) != desired_value:
            setattr(user, field_name, desired_value)
            update_fields.append(field_name)

    if is_new:
        user.can_post_in_connect = False
        user.must_change_password = False
        user.password_changed_at = timezone.now()
        user.save()
        return True

    if update_fields:
        user.save(update_fields=[*update_fields, "updated_at"])
        return True
    return False


def _apply_directory_fields(profile, user, item):
    source_status = _map_employment_status(item.get("employment_status"))
    source_visible = _directory_visibility_for_source(
        source_status,
        item.get("is_directory_visible"),
    )
    source_date_of_birth = _parse_optional_date(item.get("date_of_birth"))
    source_joined_on = _parse_optional_date(item.get("joined_on"))
    desired_values = {
        "company_name": str(item.get("company_name") or "").strip(),
        "function_name": str(item.get("function_name") or "").strip(),
        "office_location": str(item.get("office_location") or "").strip(),
        "city": str(item.get("city") or item.get("office_location") or "").strip(),
        "mobile_number": str(item.get("mobile_number") or "").strip(),
        "date_of_birth": source_date_of_birth if source_date_of_birth is not None else profile.date_of_birth,
        "joined_on": source_joined_on if source_joined_on is not None else profile.joined_on,
        "is_visible": source_visible,
        "department_for_connect": map_department_for_connect(user.department),
    }

    update_fields = []
    for field_name, desired_value in desired_values.items():
        if getattr(profile, field_name) != desired_value:
            setattr(profile, field_name, desired_value)
            update_fields.append(field_name)

    if profile._state.adding:
        profile.save()
        return True

    if update_fields:
        profile.save(update_fields=[*update_fields, "updated_at"])
        return True
    return False


def _link_managers(pending_links):
    for user_id, manager_employee_id in pending_links:
        if not manager_employee_id:
            continue
        manager = User.objects.filter(employee_code=manager_employee_id).order_by("id").first()
        if not manager:
            continue
        profile = DirectoryProfile.objects.filter(user_id=user_id).first()
        if profile and profile.manager_id != manager.id:
            profile.manager = manager
            profile.save(update_fields=["manager", "updated_at"])


def get_default_incremental_checkpoint():
    latest_run = (
        PeopleSyncRun.objects.filter(status=PeopleSyncRun.Status.SUCCESS)
        .exclude(next_updated_since__isnull=True)
        .order_by("-started_at")
        .first()
    )
    if latest_run:
        return latest_run.next_updated_since
    return None


def fetch_people_page(*, updated_since=None, cursor=None):
    base_url = str(
        getattr(settings, "PEOPLE_DIRECTORY_API_BASE_URL", "") or ""
    ).strip().rstrip("/")
    token = str(getattr(settings, "PEOPLE_DIRECTORY_API_TOKEN", "") or "").strip()
    timeout_seconds = int(
        getattr(settings, "PEOPLE_DIRECTORY_API_TIMEOUT_SECONDS", 15)
    )
    if not base_url:
        raise PeopleSyncError("PEOPLE_DIRECTORY_API_BASE_URL is not configured.")
    if not token:
        raise PeopleSyncError("PEOPLE_DIRECTORY_API_TOKEN is not configured.")

    query = {}
    if updated_since:
        query["updated_since"] = _isoformat_utc(updated_since)
    if cursor:
        query["cursor"] = str(cursor).strip()
    url = f"{base_url}/api/connect/employees"
    if query:
        url = f"{url}?{urlencode(query)}"
    _ensure_https_people_api_url(url)

    request = Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=timeout_seconds) as response:  # nosec B310
            raw_payload = response.read().decode("utf-8")
    except HTTPError as exc:
        raise PeopleSyncError(f"People API returned HTTP {exc.code}.") from exc
    except URLError as exc:
        raise PeopleSyncError("People API could not be reached.") from exc

    try:
        payload = json.loads(raw_payload)
    except json.JSONDecodeError as exc:
        raise PeopleSyncError("People API returned invalid JSON.") from exc

    if not isinstance(payload, dict):
        raise PeopleSyncError("People API returned an unexpected payload.")
    employees = payload.get("employees")
    if not isinstance(employees, list):
        raise PeopleSyncError("People API payload is missing an employees list.")
    return payload


def sync_one_employee(item):
    payload = _validate_employee_item(item)
    source_status = _map_employment_status(payload.get("employment_status"))
    manager_employee_id = str(payload.get("manager_employee_id") or "").strip()

    with transaction.atomic():
        user = _find_user_for_sync(payload["employee_id"], payload["email"])
        is_new = user is None
        if is_new:
            display_name, first_name, last_name = _split_name_parts(payload)
            user = User(
                email=payload["email"],
                first_name=first_name,
                last_name=last_name,
                display_name=display_name,
                employee_code=payload["employee_id"],
                title=str(payload.get("title") or "").strip(),
                department=str(payload.get("department") or "").strip(),
                location=str(payload.get("office_location") or payload.get("city") or "").strip(),
                phone_number=str(payload.get("mobile_number") or "").strip(),
                employment_status=User.EmploymentStatus.PENDING
                if source_status == User.EmploymentStatus.ACTIVE
                else source_status,
                is_directory_visible=_directory_visibility_for_source(
                    source_status,
                    payload.get("is_directory_visible"),
                ),
                is_active=source_status != User.EmploymentStatus.ALUMNI,
                can_post_in_connect=False,
                must_change_password=False,
                password_changed_at=timezone.now(),
            )
        user_changed = _apply_user_fields(user, payload, source_status=source_status, is_new=is_new)

        profile = getattr(user, "directory_profile", None)
        profile_created = profile is None
        if profile_created:
            profile = DirectoryProfile(user=user)
        profile_changed = _apply_directory_fields(profile, user, payload)

    return {
        "created": is_new or profile_created,
        "updated": bool(user_changed or profile_changed) and not (is_new or profile_created),
        "manager_employee_id": manager_employee_id,
        "source_updated_at": payload["source_updated_at"],
        "user_id": user.id,
    }


def run_people_sync(*, sync_type="incremental", requested_updated_since=None, fetch_page=None):
    sync_type = str(sync_type or PeopleSyncRun.SyncType.INCREMENTAL).strip().lower()
    if sync_type not in {PeopleSyncRun.SyncType.FULL, PeopleSyncRun.SyncType.INCREMENTAL}:
        raise PeopleSyncError("sync_type must be either 'full' or 'incremental'.")

    fetch_page = fetch_page or fetch_people_page
    actual_updated_since = requested_updated_since
    if sync_type == PeopleSyncRun.SyncType.FULL:
        actual_updated_since = None
    elif actual_updated_since is None:
        actual_updated_since = get_default_incremental_checkpoint()

    run = PeopleSyncRun.objects.create(
        sync_type=sync_type,
        status=PeopleSyncRun.Status.RUNNING,
        started_at=timezone.now(),
        requested_updated_since=actual_updated_since,
    )

    latest_source_updated_at = None
    pending_links = []
    cursor = None

    try:
        while True:
            response = fetch_page(updated_since=actual_updated_since, cursor=cursor)
            generated_at = response.get("generated_at")
            if generated_at:
                run.source_generated_at = _parse_iso_datetime(generated_at, "generated_at")
            employees = response.get("employees") or []

            for item in employees:
                run.records_seen += 1
                try:
                    result = sync_one_employee(item)
                except Exception as exc:
                    run.records_failed += 1
                    PeopleSyncFailure.objects.create(
                        sync_run=run,
                        employee_id=str((item or {}).get("employee_id") or "").strip(),
                        email=str((item or {}).get("email") or "").strip().lower(),
                        error_code=type(exc).__name__,
                        error_message=str(exc),
                        payload_snapshot=dict(item or {}),
                    )
                    continue

                if result["created"]:
                    run.records_created += 1
                elif result["updated"]:
                    run.records_updated += 1
                else:
                    run.records_skipped += 1

                if result["manager_employee_id"]:
                    pending_links.append((result["user_id"], result["manager_employee_id"]))
                if latest_source_updated_at is None or result["source_updated_at"] > latest_source_updated_at:
                    latest_source_updated_at = result["source_updated_at"]

            cursor = response.get("next_cursor")
            if not cursor:
                break

        _link_managers(pending_links)

        if run.records_failed == 0:
            run.status = PeopleSyncRun.Status.SUCCESS
            run.next_updated_since = latest_source_updated_at or actual_updated_since or run.source_generated_at
        elif run.records_created or run.records_updated or run.records_skipped:
            run.status = PeopleSyncRun.Status.PARTIAL_SUCCESS
            run.next_updated_since = actual_updated_since
            run.error_summary = f"{run.records_failed} employee record(s) failed during sync."
        else:
            run.status = PeopleSyncRun.Status.FAILED
            run.next_updated_since = actual_updated_since
            run.error_summary = "No employee records could be processed."
    except Exception as exc:
        run.status = PeopleSyncRun.Status.FAILED
        run.next_updated_since = actual_updated_since
        run.error_summary = str(exc)
    finally:
        run.finished_at = timezone.now()
        run.save(
            update_fields=[
                "status",
                "finished_at",
                "next_updated_since",
                "source_generated_at",
                "records_seen",
                "records_created",
                "records_updated",
                "records_skipped",
                "records_failed",
                "error_summary",
            ]
        )

    return run
