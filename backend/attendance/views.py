from datetime import date

from django.http import HttpResponseNotAllowed, JsonResponse

from .services import admin_attendance_overview, serialize_attendance_status


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
