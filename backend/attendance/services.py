from __future__ import annotations

import ipaddress
from dataclasses import dataclass
from datetime import date, timedelta

from django.conf import settings
from django.db.models import Q
from django.utils import timezone

from accounts.models import User
from directory.models import DirectoryProfile
from directory.utils import resolve_branch_location

from .holidays import holiday_for_date
from .models import AttendanceDayRecord


@dataclass(frozen=True)
class OfficeNetwork:
    label: str
    network: ipaddress._BaseNetwork


def client_ip_address(request) -> str:
    forwarded_for = str(request.META.get("HTTP_X_FORWARDED_FOR") or "").strip()
    if forwarded_for:
        return forwarded_for.split(",", 1)[0].strip()
    return str(request.META.get("REMOTE_ADDR") or "").strip()


def configured_office_networks() -> list[OfficeNetwork]:
    raw_value = str(getattr(settings, "ATTENDANCE_OFFICE_NETWORKS", "") or "").strip()
    networks = []
    for item in [part.strip() for part in raw_value.split(",") if part.strip()]:
        label = "Office"
        value = item
        if "=" in item:
            label, value = [part.strip() for part in item.split("=", 1)]
        elif ":" in item and "/" in item and item.count(":") == 1:
            label, value = [part.strip() for part in item.split(":", 1)]
        try:
            networks.append(OfficeNetwork(label=label or "Office", network=ipaddress.ip_network(value, strict=False)))
        except ValueError:
            continue
    return networks


def office_for_request(request):
    ip_text = client_ip_address(request)
    try:
        client_ip = ipaddress.ip_address(ip_text)
    except ValueError:
        return None, ip_text
    for office_network in configured_office_networks():
        if client_ip in office_network.network:
            return office_network, ip_text
    return None, ip_text


def attendance_method_for_profile(profile: DirectoryProfile | None) -> str:
    return str(getattr(profile, "attendance_recording_method", "") or "").strip()


def uses_connect_attendance(profile: DirectoryProfile | None) -> bool:
    method = attendance_method_for_profile(profile)
    if not method:
        return True
    return method.casefold() in {"connect", "connect app", "acuite connect", "connect-app"}


def branch_location_for_profile(profile: DirectoryProfile | None) -> str:
    if not profile:
        return ""
    return resolve_branch_location(
        profile.office_location,
        profile.city,
        getattr(profile.user, "location", ""),
    )


def working_day_status(target_date: date, profile: DirectoryProfile | None = None):
    holiday = holiday_for_date(target_date, location=branch_location_for_profile(profile))
    if holiday:
        return AttendanceDayRecord.Status.HOLIDAY, holiday["name"]
    if target_date.weekday() >= 5:
        return AttendanceDayRecord.Status.WEEKEND, "Weekend"
    return None, ""


def _profile_for_user(user):
    try:
        return user.directory_profile
    except DirectoryProfile.DoesNotExist:
        return None


def _status_from_record(record: AttendanceDayRecord) -> str:
    if record.status in set(AttendanceDayRecord.Status.values):
        return record.status
    if record.punch_in_at and record.punch_out_at:
        return (
            AttendanceDayRecord.Status.PRESENT
            if record.punch_out_source == AttendanceDayRecord.Source.LOGOUT
            else AttendanceDayRecord.Status.NO_PUNCHOUT
        )
    if record.punch_in_at and not record.punch_out_at:
        return AttendanceDayRecord.Status.NO_PUNCHOUT
    return AttendanceDayRecord.Status.NOT_MARKED


def _serialize_user(user):
    return {
        "id": user.id,
        "name": user.full_name,
        "email": user.email,
        "initials": user.initials,
        "title": user.title,
        "department": user.department,
    }


def serialize_attendance_status(user, *, target_date=None, record=None, request=None):
    target_date = target_date or timezone.localdate()
    profile = _profile_for_user(user)
    calendar_status, calendar_label = working_day_status(target_date, profile)
    if not uses_connect_attendance(profile):
        return {
            "user": _serialize_user(user),
            "date": target_date.isoformat(),
            "status": AttendanceDayRecord.Status.NOT_APPLICABLE,
            "status_label": "Not Applicable",
            "detail": "Attendance is not recorded through Connect for this employee.",
            "attendance_recording_method": attendance_method_for_profile(profile),
            "office_network_configured": bool(configured_office_networks()),
            "is_office_network": False,
            "calendar_label": "",
            "record": None,
        }
    if calendar_status:
        return {
            "user": _serialize_user(user),
            "date": target_date.isoformat(),
            "status": calendar_status,
            "status_label": "Holiday" if calendar_status == AttendanceDayRecord.Status.HOLIDAY else "Non-working day",
            "detail": calendar_label,
            "attendance_recording_method": attendance_method_for_profile(profile) or "Connect",
            "office_network_configured": bool(configured_office_networks()),
            "is_office_network": False,
            "calendar_label": calendar_label,
            "record": None,
        }

    record = record or AttendanceDayRecord.objects.filter(user=user, attendance_date=target_date).first()
    office_network, _ip_text = office_for_request(request) if request else (None, "")
    if not record:
        is_configured = bool(configured_office_networks())
        outside_detail = "Not marked. Outside office network."
        return {
            "user": _serialize_user(user),
            "date": target_date.isoformat(),
            "status": AttendanceDayRecord.Status.NOT_MARKED,
            "status_label": "Not Marked",
            "detail": outside_detail,
            "attendance_recording_method": "Connect",
            "office_network_configured": is_configured,
            "is_office_network": bool(office_network),
            "calendar_label": "",
            "record": None,
        }

    status = _status_from_record(record)
    detail = (
        "Punch-out has not been recorded yet."
        if status == AttendanceDayRecord.Status.NO_PUNCHOUT
        else "Attendance captured from trusted office network."
    )
    record_status = {
        AttendanceDayRecord.Status.PRESENT: "Present",
        AttendanceDayRecord.Status.NO_PUNCHOUT: "No Punchout",
        AttendanceDayRecord.Status.NOT_MARKED: "Not Marked",
    }.get(status, "Not Marked")
    return {
        "user": _serialize_user(user),
        "date": target_date.isoformat(),
        "status": status,
        "status_label": record_status,
        "detail": detail,
        "attendance_recording_method": "Connect",
        "office_network_configured": bool(configured_office_networks()),
        "is_office_network": bool(office_network),
        "calendar_label": "",
        "record": serialize_attendance_record(record),
    }


def serialize_attendance_record(record: AttendanceDayRecord):
    duration_minutes = None
    if record.punch_in_at and record.punch_out_at:
        duration_minutes = max(int((record.punch_out_at - record.punch_in_at).total_seconds() // 60), 0)
    return {
        "id": record.id,
        "user": _serialize_user(record.user),
        "date": record.attendance_date.isoformat(),
        "status": _status_from_record(record),
        "status_label": _status_from_record(record).replace("_", " ").title(),
        "punch_in_at": record.punch_in_at.isoformat() if record.punch_in_at else "",
        "punch_out_at": record.punch_out_at.isoformat() if record.punch_out_at else "",
        "punch_out_source": record.punch_out_source,
        "first_activity_at": record.first_activity_at.isoformat() if record.first_activity_at else "",
        "last_activity_at": record.last_activity_at.isoformat() if record.last_activity_at else "",
        "duration_minutes": duration_minutes,
        "office_label": record.office_label,
        "requires_regularization": _status_from_record(record) == AttendanceDayRecord.Status.NO_PUNCHOUT,
    }


def attendance_export_payload(*, from_date: date, to_date: date):
    records = {
        (record.user_id, record.attendance_date): record
        for record in AttendanceDayRecord.objects.select_related("user").filter(
            attendance_date__gte=from_date,
            attendance_date__lte=to_date,
        )
    }
    users = (
        User.objects.filter(is_active=True, employment_status=User.EmploymentStatus.ACTIVE)
        .select_related("directory_profile", "employee_sso_identity")
        .order_by("employee_code", "email")
    )

    results = []
    current_date = from_date
    while current_date <= to_date:
        for user in users:
            results.append(_serialize_attendance_export_row(user, current_date, records.get((user.id, current_date))))
        current_date += timedelta(days=1)

    return {
        "from": from_date.isoformat(),
        "to": to_date.isoformat(),
        "generated_at": timezone.now().isoformat(),
        "records": results,
    }


def attendance_employee_day_export_payload(
    *,
    attendance_date: date,
    employee_sso_id="",
    employee_code="",
    email="",
):
    user = _attendance_export_user(
        employee_sso_id=employee_sso_id,
        employee_code=employee_code,
        email=email,
    )
    records = []
    if user:
        record = AttendanceDayRecord.objects.filter(
            user=user,
            attendance_date=attendance_date,
        ).first()
        records.append(_serialize_attendance_export_row(user, attendance_date, record))

    return {
        "date": attendance_date.isoformat(),
        "generated_at": timezone.now().isoformat(),
        "records": records,
    }


def _serialize_attendance_export_row(user, attendance_date, record=None):
    profile = _profile_for_user(user)
    identity = getattr(user, "employee_sso_identity", None)
    calendar_status, calendar_label = working_day_status(attendance_date, profile)
    status = AttendanceDayRecord.Status.NOT_MARKED
    source = AttendanceDayRecord.Source.SYSTEM
    requires_regularization = True
    punch_in_at = ""
    punch_out_at = ""
    office_label = ""
    updated_at = timezone.now()

    if not uses_connect_attendance(profile):
        status = AttendanceDayRecord.Status.NOT_APPLICABLE
        requires_regularization = False
    elif calendar_status:
        status = calendar_status
        requires_regularization = False
    elif record:
        status = _status_from_record(record)
        source = record.punch_out_source or record.punch_in_source or AttendanceDayRecord.Source.SYSTEM
        requires_regularization = status in {
            AttendanceDayRecord.Status.NO_PUNCHOUT,
            AttendanceDayRecord.Status.NOT_MARKED,
        }
        punch_in_at = record.punch_in_at.isoformat() if record.punch_in_at else ""
        punch_out_at = (
            record.punch_out_at.isoformat()
            if record.punch_out_at and status != AttendanceDayRecord.Status.NO_PUNCHOUT
            else ""
        )
        office_label = record.office_label
        updated_at = record.updated_at

    return {
        "employee_sso_id": getattr(identity, "sso_user_id", "") or "",
        "employee_code": user.employee_code or getattr(identity, "employee_id", "") or "",
        "email": user.email,
        "attendance_date": attendance_date.isoformat(),
        "punch_in_at": punch_in_at,
        "punch_out_at": punch_out_at,
        "status": status,
        "status_label": status.replace("_", " ").title(),
        "source": source,
        "office_label": office_label or calendar_label,
        "requires_regularization": requires_regularization,
        "updated_at": updated_at.isoformat(),
    }


def _attendance_export_user(*, employee_sso_id="", employee_code="", email=""):
    users = (
        User.objects.filter(is_active=True, employment_status=User.EmploymentStatus.ACTIVE)
        .select_related("directory_profile", "employee_sso_identity")
        .order_by("employee_code", "email")
    )
    employee_sso_id = str(employee_sso_id or "").strip()
    employee_code = str(employee_code or "").strip()
    email = str(email or "").strip()
    if employee_sso_id:
        user = users.filter(employee_sso_identity__sso_user_id=employee_sso_id).first()
        if user:
            return user
    if employee_code:
        user = users.filter(
            Q(employee_code__iexact=employee_code)
            | Q(employee_sso_identity__employee_id__iexact=employee_code)
        ).first()
        if user:
            return user
    if email:
        return users.filter(Q(email__iexact=email) | Q(employee_sso_identity__email__iexact=email)).first()
    return None


def capture_attendance_activity(request, *, source="activity"):
    user = getattr(request, "user", None)
    if not getattr(user, "is_authenticated", False):
        return None
    if not getattr(user, "has_employee_access", True):
        return None

    today = timezone.localdate()
    profile = _profile_for_user(user)
    calendar_status, _calendar_label = working_day_status(today, profile)
    if calendar_status:
        return None

    if not uses_connect_attendance(profile):
        return None

    office_network, ip_text = office_for_request(request)
    if not office_network:
        return None

    now = timezone.now()
    record, _created = AttendanceDayRecord.objects.get_or_create(
        user=user,
        attendance_date=today,
        defaults={
            "status": AttendanceDayRecord.Status.NO_PUNCHOUT,
            "punch_in_at": now,
            "first_activity_at": now,
            "office_label": office_network.label,
            "punch_in_ip": ip_text,
            "punch_in_source": AttendanceDayRecord.Source.ACTIVITY,
        },
    )
    update_fields = []
    if not record.punch_in_at:
        record.punch_in_at = now
        record.punch_in_ip = ip_text
        record.punch_in_source = AttendanceDayRecord.Source.ACTIVITY
        update_fields.extend(["punch_in_at", "punch_in_ip", "punch_in_source"])
    if not record.first_activity_at:
        record.first_activity_at = now
        update_fields.append("first_activity_at")
    record.last_activity_at = now
    record.last_activity_ip = ip_text
    record.office_label = office_network.label
    record.punch_out_at = now
    punch_out_source = (
        AttendanceDayRecord.Source.LOGOUT
        if source == "logout"
        else AttendanceDayRecord.Source.ACTIVITY
    )
    record.punch_out_source = punch_out_source
    record.status = (
        AttendanceDayRecord.Status.PRESENT
        if punch_out_source == AttendanceDayRecord.Source.LOGOUT
        else AttendanceDayRecord.Status.NO_PUNCHOUT
    )
    record.requires_regularization = record.status == AttendanceDayRecord.Status.NO_PUNCHOUT
    update_fields.extend([
        "last_activity_at",
        "last_activity_ip",
        "office_label",
        "punch_out_at",
        "punch_out_source",
        "status",
        "requires_regularization",
    ])
    record.save(update_fields=[*dict.fromkeys(update_fields), "updated_at"])
    return record


def admin_attendance_overview(*, target_date=None, request=None):
    target_date = target_date or timezone.localdate()
    records = {
        record.user_id: record
        for record in AttendanceDayRecord.objects.select_related("user").filter(attendance_date=target_date)
    }
    users = (
        User.objects.filter(is_active=True, employment_status=User.EmploymentStatus.ACTIVE)
        .select_related("directory_profile")
        .order_by("display_name", "email")
    )
    rows = [
        serialize_attendance_status(user, target_date=target_date, record=records.get(user.id), request=request)
        for user in users
    ]
    counts = {}
    for row in rows:
        counts[row["status"]] = counts.get(row["status"], 0) + 1
    return {
        "date": target_date.isoformat(),
        "office_network_configured": bool(configured_office_networks()),
        "counts": counts,
        "results": rows,
    }
