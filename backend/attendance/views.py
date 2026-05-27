import secrets
from datetime import date, timedelta

from django.conf import settings
from django.http import HttpResponseNotAllowed, JsonResponse

from .services import (
    attendance_employee_day_export_payload,
    attendance_export_payload,
    admin_attendance_overview,
    serialize_attendance_status,
)


def _is_attendance_admin(user):
    return user.is_authenticated and (
        user.is_superuser
        or getattr(user, "access_level", "") == "admin"
        or user.has_perm("attendance.view_attendance_admin")
    )


def _parse_date(value):
    raw_value = str(value or "").strip()
    if not raw_value:
        return None
    return date.fromisoformat(raw_value)


def _service_token_allowed(request):
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return False
    token = auth_header.split(" ", 1)[1].strip()
    return any(
        secrets.compare_digest(token, allowed_token)
        for allowed_token in getattr(settings, "CONNECT_ATTENDANCE_EXPORT_TOKENS", [])
    )


def attendance_status(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    return JsonResponse(serialize_attendance_status(request.user, request=request))


def attendance_admin_overview(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    if not _is_attendance_admin(request.user):
        return JsonResponse({"detail": "Admin access required."}, status=403)
    try:
        target_date = _parse_date(request.GET.get("date"))
    except ValueError:
        return JsonResponse({"detail": "Date must be in YYYY-MM-DD format."}, status=400)
    return JsonResponse(admin_attendance_overview(target_date=target_date, request=request))


def attendance_export(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    if not _service_token_allowed(request):
        return JsonResponse({"detail": "Valid service token required."}, status=401)
    try:
        from_date = _parse_date(request.GET.get("from"))
        to_date = _parse_date(request.GET.get("to"))
    except ValueError:
        return JsonResponse({"detail": "from and to must be in YYYY-MM-DD format."}, status=400)
    if not from_date or not to_date:
        return JsonResponse({"detail": "from and to are required."}, status=400)
    if to_date < from_date:
        return JsonResponse({"detail": "to must be on or after from."}, status=400)
    if to_date - from_date > timedelta(days=62):
        return JsonResponse({"detail": "Date range cannot exceed 63 days."}, status=400)
    return JsonResponse(attendance_export_payload(from_date=from_date, to_date=to_date))


def attendance_employee_day_export(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    if not _service_token_allowed(request):
        return JsonResponse({"detail": "Valid service token required."}, status=401)
    try:
        attendance_date = _parse_date(request.GET.get("date") or request.GET.get("attendance_date"))
    except ValueError:
        return JsonResponse({"detail": "date must be in YYYY-MM-DD format."}, status=400)
    if not attendance_date:
        return JsonResponse({"detail": "date is required."}, status=400)

    employee_sso_id = request.GET.get("employee_sso_id", "")
    employee_code = request.GET.get("employee_code", "")
    email = request.GET.get("email", "")
    if not any(str(value or "").strip() for value in [employee_sso_id, employee_code, email]):
        return JsonResponse(
            {"detail": "employee_sso_id, employee_code, or email is required."},
            status=400,
        )

    return JsonResponse(
        attendance_employee_day_export_payload(
            attendance_date=attendance_date,
            employee_sso_id=employee_sso_id,
            employee_code=employee_code,
            email=email,
        )
    )
