import json
from datetime import date
from urllib.parse import urlencode, urlparse

from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from directory.models import DirectoryProfile
from operations.services import record_analytics_event, record_audit_event

from .models import ExitProcess, User
from .session import ensure_session_deadline
from .serializers import serialize_exit_process, serialize_user
from .services import (
    AuthFlowError,
    SESSION_AUTH_BACKEND,
    begin_employee_sso_login,
    change_password_after_challenge,
    complete_login,
    complete_employee_sso_login,
    employee_sso_enabled,
    employee_sso_logout_redirect,
    exchange_trusted_sso_grant,
    get_trusted_sso_client,
    issue_trusted_sso_grant,
    normalize_email,
    reset_password_to_first_time_password,
    start_login_challenge,
    validate_trusted_redirect_uri,
    validate_password_step,
    verify_login_otp,
)


def _parse_json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise AuthFlowError("Request body must be valid JSON.", status=400, code="invalid_json") from exc


def _auth_policy_payload():
    return {
        "mode": "employee_sso" if employee_sso_enabled() else "manual_accounts_with_email_otp_and_password",
        "password_max_age_days": settings.AUTH_PASSWORD_MAX_AGE_DAYS,
        "otp_ttl_minutes": settings.AUTH_OTP_TTL_MINUTES,
        "otp_code_length": settings.AUTH_OTP_CODE_LENGTH,
        "account_provisioning": "manual_admin_control",
        "employee_sso_enabled": employee_sso_enabled(),
        "employee_sso_start_path": "/api/accounts/auth/employee-sso/start/",
    }


def _error_response(exc):
    payload = {"detail": exc.message, "code": exc.code}
    payload.update(exc.extra)
    return JsonResponse(payload, status=exc.status)


def _admin_forbidden(detail="Admin access required."):
    return JsonResponse({"detail": detail}, status=403)


def _is_access_admin(user):
    return user.is_authenticated and (
        getattr(user, "can_manage_access_rights", False)
        or user.is_superuser
        or user.has_perm("accounts.manage_access_rights")
    )


def _coerce_bool(value):
    if isinstance(value, bool):
        return value
    return str(value or "").strip().lower() in {"1", "true", "yes", "y", "on"}


def _safe_next_path(raw_value, fallback="/"):
    candidate = str(raw_value or "").strip()
    if not candidate:
        return fallback
    parsed = urlparse(candidate)
    if parsed.scheme or parsed.netloc:
        return fallback
    if not candidate.startswith("/"):
        return fallback
    return candidate


def _split_display_name(display_name, fallback_email=""):
    cleaned = str(display_name or "").strip()
    if not cleaned and fallback_email:
        cleaned = fallback_email.split("@", 1)[0].replace(".", " ").replace("_", " ").title()
    parts = [part for part in cleaned.split() if part]
    if not parts:
        return "", "", ""
    if len(parts) == 1:
        return cleaned, parts[0], ""
    return cleaned, parts[0], " ".join(parts[1:])


def _company_name_for_email(email):
    domain = str(email or "").strip().lower().split("@")[-1]
    if domain == "smera.in":
        return "SMERA"
    if domain == "esgrisk.ai":
        return "ESGRisk.ai"
    return "Acuite"


def _sync_directory_profile(user, payload):
    existing_profile = getattr(user, "directory_profile", None)
    DirectoryProfile.objects.update_or_create(
        user=user,
        defaults={
            "company_name": str(
                payload.get("company_name")
                or (existing_profile.company_name if existing_profile else "")
                or _company_name_for_email(user.email)
            ).strip(),
            "function_name": str(
                payload.get("function_name")
                or (existing_profile.function_name if existing_profile else "")
            ).strip(),
            "office_location": str(
                payload.get("office_location")
                or payload.get("location")
                or (existing_profile.office_location if existing_profile else user.location)
            ).strip(),
            "city": str(
                payload.get("city")
                or payload.get("location")
                or (existing_profile.city if existing_profile else user.location)
            ).strip(),
            "mobile_number": str(
                payload.get("mobile_number")
                or payload.get("phone_number")
                or (existing_profile.mobile_number if existing_profile else user.phone_number)
            ).strip(),
            "is_visible": True,
        },
    )


def _password_change_reason(user):
    if user.must_change_password or not user.password_changed_at:
        return "first_login"
    return "expired"


def _parse_iso_date(value, field_label):
    raw_value = str(value or "").strip()
    if not raw_value:
        raise AuthFlowError(f"{field_label} is required.", status=400, code="missing_date")
    try:
        return date.fromisoformat(raw_value)
    except ValueError as exc:
        raise AuthFlowError(
            f"{field_label} must be a valid date in YYYY-MM-DD format.",
            status=400,
            code="invalid_date",
        ) from exc


def _apply_alumni_transition(process, actor):
    employee = process.employee
    user_update_fields = []
    if employee.employment_status != User.EmploymentStatus.ALUMNI:
        employee.employment_status = User.EmploymentStatus.ALUMNI
        user_update_fields.append("employment_status")
    if employee.is_active:
        employee.is_active = False
        user_update_fields.append("is_active")
    if employee.can_post_in_connect:
        employee.can_post_in_connect = False
        user_update_fields.append("can_post_in_connect")
    if employee.is_directory_visible:
        employee.is_directory_visible = False
        user_update_fields.append("is_directory_visible")
    if employee.access_level != User.AccessLevel.EMPLOYEE:
        employee.access_level = User.AccessLevel.EMPLOYEE
        user_update_fields.append("access_level")
    if user_update_fields:
        employee.save(update_fields=[*user_update_fields, "updated_at"])

    if hasattr(employee, "directory_profile"):
        directory_profile = employee.directory_profile
        if directory_profile.is_visible:
            directory_profile.is_visible = False
            directory_profile.save(update_fields=["is_visible", "updated_at"])

    process.updated_by = actor
    process.mark_completed()
    process.save(
        update_fields=[
            "updated_by",
            "stage",
            "alumni_transition_completed",
            "completed_at",
            "updated_at",
        ]
    )


def _authenticated_payload(request, *, password_changed=False):
    session_deadline = ensure_session_deadline(request)
    return {
        "authenticated": True,
        "user": serialize_user(request.user),
        # Access decisions come from the serialized role flags; enumerating every
        # Django permission here adds avoidable auth queries to the login path.
        "permissions": [],
        "password_changed": password_changed,
        "auth_policy": _auth_policy_payload(),
        "session_expires_at": session_deadline.isoformat() if session_deadline else None,
    }


def current_user(request):
    if request.user.is_authenticated:
        return JsonResponse(_authenticated_payload(request))

    return JsonResponse(
        {
            "authenticated": False,
            "user": None,
            "permissions": [],
            "next_auth_decision": (
                ["employee_sso"]
                if employee_sso_enabled()
                else [
                    "manual_employee_account",
                    "email_otp",
                    "password_with_rotation",
                ]
            ),
            "auth_policy": _auth_policy_payload(),
            "session_expires_at": None,
        }
    )


def access_user_collection(request):
    if not _is_access_admin(request.user):
        return _admin_forbidden()

    if request.method == "POST":
        try:
            payload = _parse_json_body(request)
        except AuthFlowError as exc:
            return _error_response(exc)

        email = normalize_email(payload.get("email"))
        if not email:
            return JsonResponse({"detail": "Email is required."}, status=400)
        try:
            validate_email(email)
        except ValidationError:
            return JsonResponse({"detail": "Enter a valid employee email ID."}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"detail": "An employee account with this email already exists."}, status=409)

        access_level = str(payload.get("access_level") or User.AccessLevel.EMPLOYEE).strip().lower()
        allowed_access_levels = {
            User.AccessLevel.EMPLOYEE,
            User.AccessLevel.MODERATOR,
            User.AccessLevel.ADMIN,
        }
        if access_level not in allowed_access_levels:
            return JsonResponse({"detail": "Invalid access level supplied."}, status=400)

        employment_status = str(
            payload.get("employment_status") or User.EmploymentStatus.ACTIVE
        ).strip().lower()
        if employment_status not in set(User.EmploymentStatus.values):
            return JsonResponse({"detail": "Invalid employment status supplied."}, status=400)

        display_name, first_name, last_name = _split_display_name(
            payload.get("display_name") or payload.get("name"),
            email,
        )
        temporary_password = str(
            payload.get("temporary_password") or settings.AUTH_FIRST_TIME_PASSWORD
        ).strip() or settings.AUTH_FIRST_TIME_PASSWORD

        user = User.objects.create_user(
            email=email,
            password=temporary_password,
            first_name=first_name,
            last_name=last_name,
            display_name=display_name,
            employee_code=str(payload.get("employee_code") or "").strip(),
            title=str(payload.get("title") or "").strip(),
            department=str(payload.get("department") or "").strip(),
            location=str(payload.get("location") or "").strip(),
            phone_number=str(payload.get("phone_number") or "").strip(),
            access_level=access_level,
            employment_status=employment_status,
            can_post_in_connect=_coerce_bool(payload.get("can_post_in_connect", True)),
            is_active=_coerce_bool(payload.get("is_active", True)),
            must_change_password=True,
            password_changed_at=None,
        )
        _sync_directory_profile(user, payload)

        record_audit_event(
            action="accounts.user.created",
            actor=request.user,
            target=user,
            summary=f"Created employee account for {user.email}",
            metadata={
                "access_level": user.access_level,
                "employment_status": user.employment_status,
                "can_post_in_connect": user.can_post_in_connect,
            },
            request=request,
        )
        record_analytics_event(
            "accounts",
            "user_created",
            actor=request.user,
            metadata={"target_user_id": user.id, "access_level": user.access_level},
            request=request,
        )
        return JsonResponse(
            {
                "detail": "Employee account created successfully.",
                "user": serialize_user(user),
            },
            status=201,
        )

    if request.method != "GET":
        return HttpResponseNotAllowed(["GET", "POST"])

    query = str(request.GET.get("q", "")).strip()
    queryset = User.objects.order_by("display_name", "email")
    if query:
        queryset = queryset.filter(
            models.Q(email__icontains=query)
            | models.Q(first_name__icontains=query)
            | models.Q(last_name__icontains=query)
            | models.Q(display_name__icontains=query)
            | models.Q(employee_code__icontains=query)
            | models.Q(title__icontains=query)
            | models.Q(department__icontains=query)
        )

    results = [serialize_user(user) for user in queryset[:200]]
    return JsonResponse(
        {
            "count": len(results),
            "results": results,
            "available_access_levels": [
                User.AccessLevel.EMPLOYEE,
                User.AccessLevel.MODERATOR,
                User.AccessLevel.ADMIN,
            ],
        }
    )


@csrf_exempt
def access_user_detail(request, user_id):
    if request.method not in {"GET", "POST", "PATCH"}:
        return HttpResponseNotAllowed(["GET", "POST", "PATCH"])
    if not _is_access_admin(request.user):
        return _admin_forbidden()

    user = get_object_or_404(User, pk=user_id)
    if request.method == "GET":
        return JsonResponse({"user": serialize_user(user)})

    if user.is_superuser and not request.user.is_superuser:
        return _admin_forbidden("Only a superuser can modify this account.")
    if request.user.pk == user.pk and not request.user.is_superuser:
        return _admin_forbidden("You cannot edit your own access rights from this screen.")

    try:
        payload = _parse_json_body(request)
    except AuthFlowError as exc:
        return _error_response(exc)

    changes = {}
    update_fields = []
    profile_fields_supplied = any(
        field in payload
        for field in {"company_name", "function_name", "office_location", "city", "mobile_number"}
    )

    if "access_level" in payload:
        access_level = str(payload.get("access_level") or "").strip().lower()
        allowed_access_levels = {
            User.AccessLevel.EMPLOYEE,
            User.AccessLevel.MODERATOR,
            User.AccessLevel.ADMIN,
        }
        if access_level not in allowed_access_levels:
            return JsonResponse({"detail": "Invalid access level supplied."}, status=400)
        if user.access_level != access_level:
            changes["access_level"] = {"from": user.access_level, "to": access_level}
            user.access_level = access_level
            update_fields.append("access_level")

    if "can_post_in_connect" in payload:
        requested_can_post = _coerce_bool(payload.get("can_post_in_connect"))
        if user.can_post_in_connect != requested_can_post:
            changes["can_post_in_connect"] = {
                "from": user.can_post_in_connect,
                "to": requested_can_post,
            }
            user.can_post_in_connect = requested_can_post
            update_fields.append("can_post_in_connect")

    editable_user_fields = {
        "title": "title",
        "department": "department",
        "location": "location",
        "employee_code": "employee_code",
        "phone_number": "phone_number",
    }
    for payload_field, model_field in editable_user_fields.items():
        if payload_field not in payload:
            continue
        new_value = str(payload.get(payload_field) or "").strip()
        if getattr(user, model_field) != new_value:
            changes[model_field] = {"from": getattr(user, model_field), "to": new_value}
            setattr(user, model_field, new_value)
            update_fields.append(model_field)

    if "display_name" in payload:
        display_name, first_name, last_name = _split_display_name(payload.get("display_name"), user.email)
        if user.display_name != display_name:
            changes["display_name"] = {"from": user.display_name, "to": display_name}
            user.display_name = display_name
            update_fields.append("display_name")
        if user.first_name != first_name:
            changes["first_name"] = {"from": user.first_name, "to": first_name}
            user.first_name = first_name
            update_fields.append("first_name")
        if user.last_name != last_name:
            changes["last_name"] = {"from": user.last_name, "to": last_name}
            user.last_name = last_name
            update_fields.append("last_name")

    if "employment_status" in payload:
        employment_status = str(payload.get("employment_status") or "").strip().lower()
        if employment_status not in set(User.EmploymentStatus.values):
            return JsonResponse({"detail": "Invalid employment status supplied."}, status=400)
        if user.employment_status != employment_status:
            changes["employment_status"] = {"from": user.employment_status, "to": employment_status}
            user.employment_status = employment_status
            update_fields.append("employment_status")

    if "is_active" in payload:
        requested_is_active = _coerce_bool(payload.get("is_active"))
        if user.is_active != requested_is_active:
            changes["is_active"] = {"from": user.is_active, "to": requested_is_active}
            user.is_active = requested_is_active
            update_fields.append("is_active")

    if not update_fields and not profile_fields_supplied and "location" not in payload and "phone_number" not in payload:
        return JsonResponse({"user": serialize_user(user), "detail": "No access changes were applied."})

    if update_fields:
        update_fields.append("updated_at")
        user.save(update_fields=list(dict.fromkeys(update_fields)))

    if profile_fields_supplied or "location" in payload or "phone_number" in payload:
        _sync_directory_profile(user, payload)

    record_audit_event(
        action="accounts.access.updated",
        actor=request.user,
        target=user,
        summary=f"Updated access rights for {user.email}",
        metadata={"changes": changes},
        request=request,
    )
    record_analytics_event(
        "accounts",
        "access_updated",
        actor=request.user,
        metadata={"target_user_id": user.id, "changes": changes},
        request=request,
    )
    return JsonResponse(
        {
            "detail": "Employee account updated successfully.",
            "user": serialize_user(user),
        }
    )


@csrf_exempt
def exit_process_collection(request):
    if not _is_access_admin(request.user):
        return _admin_forbidden()

    if request.method == "POST":
        try:
            payload = _parse_json_body(request)
        except AuthFlowError as exc:
            return _error_response(exc)

        employee_id = int(payload.get("employee_id") or 0)
        if not employee_id:
            return JsonResponse({"detail": "Employee selection is required."}, status=400)

        employee = get_object_or_404(User, pk=employee_id)
        if employee.is_superuser and not request.user.is_superuser:
            return _admin_forbidden("Only a superuser can start an exit process for this account.")

        try:
            resignation_date = _parse_iso_date(payload.get("resignation_date"), "Resignation date")
            last_working_day = _parse_iso_date(payload.get("last_working_day"), "Last working day")
        except AuthFlowError as exc:
            return _error_response(exc)

        if last_working_day < resignation_date:
            return JsonResponse(
                {"detail": "Last working day cannot be earlier than the resignation date."},
                status=400,
            )

        requested_stage = str(
            payload.get("stage") or ExitProcess.Stage.NOTICE_RECEIVED
        ).strip().lower()
        if requested_stage not in set(ExitProcess.Stage.values):
            return JsonResponse({"detail": "Invalid exit stage supplied."}, status=400)

        process, created = ExitProcess.objects.get_or_create(
            employee=employee,
            defaults={
                "initiated_by": request.user,
                "updated_by": request.user,
                "resignation_date": resignation_date,
                "last_working_day": last_working_day,
                "stage": requested_stage,
                "resignation_acknowledged": _coerce_bool(payload.get("resignation_acknowledged")),
                "knowledge_transfer_completed": _coerce_bool(payload.get("knowledge_transfer_completed")),
                "assets_returned": _coerce_bool(payload.get("assets_returned")),
                "access_review_completed": _coerce_bool(payload.get("access_review_completed")),
                "alumni_transition_completed": False,
                "notes": str(payload.get("notes") or "").strip(),
            },
        )

        changes = {}
        update_fields = []
        field_map = {
            "resignation_date": resignation_date,
            "last_working_day": last_working_day,
            "stage": requested_stage,
            "resignation_acknowledged": _coerce_bool(payload.get("resignation_acknowledged")),
            "knowledge_transfer_completed": _coerce_bool(payload.get("knowledge_transfer_completed")),
            "assets_returned": _coerce_bool(payload.get("assets_returned")),
            "access_review_completed": _coerce_bool(payload.get("access_review_completed")),
            "notes": str(payload.get("notes") or "").strip(),
        }

        if not created:
            for field_name, new_value in field_map.items():
                current_value = getattr(process, field_name)
                if current_value != new_value:
                    changes[field_name] = {"from": current_value, "to": new_value}
                    setattr(process, field_name, new_value)
                    update_fields.append(field_name)

            if update_fields:
                process.updated_by = request.user
                update_fields.extend(["updated_by", "updated_at"])
                process.save(update_fields=list(dict.fromkeys(update_fields)))

        finalize = _coerce_bool(payload.get("finalize")) or requested_stage == ExitProcess.Stage.COMPLETED
        if finalize:
            if not process.can_finalize:
                return JsonResponse(
                    {
                        "detail": (
                            "Complete resignation acknowledgement, knowledge transfer, asset return "
                            "and access review before converting the employee to alumni state."
                        )
                    },
                    status=400,
                )
            _apply_alumni_transition(process, request.user)

        record_audit_event(
            action=(
                "accounts.exit_process.completed"
                if finalize
                else "accounts.exit_process.created" if created else "accounts.exit_process.updated"
            ),
            actor=request.user,
            target=employee,
            summary=(
                f"Completed exit process for {employee.email}"
                if finalize
                else f"Started exit process for {employee.email}"
                if created
                else f"Updated exit process for {employee.email}"
            ),
            metadata={
                "exit_process_id": process.id,
                "stage": process.stage,
                "changes": changes,
                "finalized": finalize,
            },
            request=request,
        )
        record_analytics_event(
            "accounts",
            "exit_process_saved",
            actor=request.user,
            metadata={
                "exit_process_id": process.id,
                "employee_user_id": employee.id,
                "stage": process.stage,
                "created": created,
                "finalized": finalize,
            },
            request=request,
        )
        return JsonResponse(
            {
                "detail": (
                    "Employee converted to alumni state."
                    if finalize
                    else "Exit process created."
                    if created
                    else "Exit process updated."
                ),
                "exit_process": serialize_exit_process(process),
            },
            status=201 if created else 200,
        )

    if request.method != "GET":
        return HttpResponseNotAllowed(["GET", "POST"])

    query = str(request.GET.get("q", "")).strip()
    status_filter = str(request.GET.get("status") or "open").strip().lower()
    queryset = ExitProcess.objects.select_related("employee").order_by("-updated_at", "-created_at")
    if status_filter == "open":
        queryset = queryset.exclude(stage=ExitProcess.Stage.COMPLETED)
    elif status_filter == "completed":
        queryset = queryset.filter(stage=ExitProcess.Stage.COMPLETED)

    if query:
        queryset = queryset.filter(
            models.Q(employee__email__icontains=query)
            | models.Q(employee__first_name__icontains=query)
            | models.Q(employee__last_name__icontains=query)
            | models.Q(employee__display_name__icontains=query)
            | models.Q(employee__employee_code__icontains=query)
            | models.Q(notes__icontains=query)
        )

    results = [serialize_exit_process(process) for process in queryset[:100]]
    return JsonResponse(
        {
            "count": len(results),
            "results": results,
            "stages": [
                ExitProcess.Stage.NOTICE_RECEIVED,
                ExitProcess.Stage.KNOWLEDGE_TRANSFER,
                ExitProcess.Stage.CLEARANCE,
                ExitProcess.Stage.ALUMNI_CONVERSION,
                ExitProcess.Stage.COMPLETED,
            ],
        }
    )


def request_login_otp(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        payload = _parse_json_body(request)
        challenge, preview_code = start_login_challenge(payload.get("email"))
    except AuthFlowError as exc:
        return _error_response(exc)

    record_audit_event(
        action="auth.otp.requested",
        actor=challenge.user,
        target=challenge.user,
        summary=f"Login OTP requested for {challenge.email}",
        metadata={"challenge_id": str(challenge.public_id)},
        request=request,
    )
    record_analytics_event(
        "auth",
        "otp_requested",
        actor=challenge.user,
        metadata={"challenge_id": str(challenge.public_id)},
        request=request,
    )
    response = {
        "detail": f"OTP is on its way to {challenge.masked_email}.",
        "challenge_token": str(challenge.public_id),
        "masked_email": challenge.masked_email,
        "next_step": "otp",
    }
    if preview_code:
        response["preview_code"] = preview_code
    return JsonResponse(response, status=201)


def forgot_password(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        payload = _parse_json_body(request)
        user = reset_password_to_first_time_password(payload.get("email"))
    except AuthFlowError as exc:
        return _error_response(exc)

    if user:
        record_audit_event(
            action="auth.password.reset_emailed",
            actor=user,
            target=user,
            summary=f"Temporary password emailed to {user.email}",
            request=request,
        )
        record_analytics_event(
            "auth",
            "password_reset_emailed",
            actor=user,
            request=request,
        )

    return JsonResponse(
        {
            "detail": "If the email is provisioned, the temporary password has been emailed. Request a fresh OTP, then log in and change your password.",
        }
    )


def verify_login_code(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        payload = _parse_json_body(request)
        challenge = verify_login_otp(payload.get("challenge_token"), payload.get("otp"))
    except AuthFlowError as exc:
        return _error_response(exc)

    record_audit_event(
        action="auth.otp.verified",
        actor=challenge.user,
        target=challenge.user,
        summary=f"Login OTP verified for {challenge.email}",
        metadata={"challenge_id": str(challenge.public_id)},
        request=request,
    )
    record_analytics_event(
        "auth",
        "otp_verified",
        actor=challenge.user,
        metadata={"challenge_id": str(challenge.public_id)},
        request=request,
    )
    return JsonResponse(
        {
            "detail": "OTP verified. Enter your password to continue.",
            "challenge_token": str(challenge.public_id),
            "next_step": "password",
        }
    )


def login_with_password(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        payload = _parse_json_body(request)
        challenge = validate_password_step(
            payload.get("challenge_token"),
            payload.get("password"),
        )
    except AuthFlowError as exc:
        return _error_response(exc)

    user = challenge.user
    if user.password_change_required:
        record_analytics_event(
            "auth",
            "password_change_required",
            actor=user,
            metadata={
                "challenge_id": str(challenge.public_id),
                "reason": _password_change_reason(user),
            },
            request=request,
        )
        return JsonResponse(
            {
                "detail": "Password change required before login can complete.",
                "challenge_token": str(challenge.public_id),
                "requires_password_change": True,
                "reason": _password_change_reason(user),
                "password_policy": {
                    "max_age_days": settings.AUTH_PASSWORD_MAX_AGE_DAYS,
                },
            }
        )

    try:
        user = complete_login(str(challenge.public_id))
    except AuthFlowError as exc:
        return _error_response(exc)

    user.backend = SESSION_AUTH_BACKEND
    auth_login(request, user)
    ensure_session_deadline(request, reset=True)
    record_audit_event(
        action="auth.login.completed",
        actor=user,
        target=user,
        summary=f"Login completed for {user.email}",
        request=request,
    )
    record_analytics_event(
        "auth",
        "login_completed",
        actor=user,
        request=request,
    )
    return JsonResponse(_authenticated_payload(request))


def change_password_and_login(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        payload = _parse_json_body(request)
        new_password = str(payload.get("new_password", ""))
        confirm_password = str(payload.get("confirm_password", ""))
        if new_password != confirm_password:
            raise AuthFlowError(
                "New password and confirmation do not match.",
                status=400,
                code="password_confirmation_mismatch",
            )
        user = change_password_after_challenge(payload.get("challenge_token"), new_password)
    except AuthFlowError as exc:
        return _error_response(exc)

    user.backend = SESSION_AUTH_BACKEND
    auth_login(request, user)
    ensure_session_deadline(request, reset=True)
    record_audit_event(
        action="auth.password.changed",
        actor=user,
        target=user,
        summary=f"Password changed during login for {user.email}",
        request=request,
    )
    record_analytics_event(
        "auth",
        "password_changed_during_login",
        actor=user,
        request=request,
    )
    return JsonResponse(_authenticated_payload(request, password_changed=True))


def logout_view(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    actor = request.user if request.user.is_authenticated else None
    if actor:
        record_audit_event(
            action="auth.logout",
            actor=actor,
            target=actor,
            summary=f"Logout completed for {normalize_email(actor.email)}",
            request=request,
        )
        record_analytics_event(
            "auth",
            "logout",
            actor=actor,
            request=request,
        )

    auth_logout(request)
    return JsonResponse(
        {
            "authenticated": False,
            "detail": "Logged out successfully.",
            "redirect_url": employee_sso_logout_redirect(),
        }
    )


def employee_sso_start(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    try:
        redirect_url = begin_employee_sso_login(
            request,
            next_path=_safe_next_path(request.GET.get("next"), "/"),
        )
    except AuthFlowError as exc:
        return _error_response(exc)
    return redirect(redirect_url)


def employee_sso_callback(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    error_code = str(request.GET.get("error") or "").strip()
    if error_code:
        detail = str(request.GET.get("error_description") or "Employee SSO login was cancelled.").strip()
        return redirect(f"/login.html?{urlencode({'error': detail})}")

    try:
        outcome = complete_employee_sso_login(
            request,
            code=request.GET.get("code"),
            state=request.GET.get("state"),
        )
    except AuthFlowError as exc:
        return redirect(f"/login.html?{urlencode({'error': exc.message})}")

    user = outcome["user"]
    user.backend = SESSION_AUTH_BACKEND
    auth_login(request, user)
    ensure_session_deadline(request, reset=True)
    record_audit_event(
        action="auth.employee_sso.login_completed",
        actor=user,
        target=user,
        summary=f"Employee SSO login completed for {user.email}",
        metadata={
            "employee_sso_user_id": outcome["identity"]["user_id"],
            "provisioned_local_user": outcome["created"],
        },
        request=request,
    )
    record_analytics_event(
        "auth",
        "employee_sso_login_completed",
        actor=user,
        metadata={"provisioned_local_user": outcome["created"]},
        request=request,
    )
    if not getattr(user, "has_employee_access", False):
        return redirect("/access-denied.html")
    return redirect(_safe_next_path(outcome["next_path"], "/"))


def sso_authorize(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    try:
        client_id, client = get_trusted_sso_client(request.GET.get("client_id"))
        redirect_uri = validate_trusted_redirect_uri(client, request.GET.get("redirect_uri"))
    except AuthFlowError as exc:
        return _error_response(exc)

    state = str(request.GET.get("state", "")).strip()
    if not request.user.is_authenticated:
        login_target = f"{settings.LOGIN_URL}?{urlencode({'next': request.get_full_path()})}"
        return redirect(login_target)

    if not request.user.login_allowed:
        return JsonResponse(
            {
                "detail": "This account is not currently active for Acuité Connect.",
                "code": "user_inactive",
            },
            status=403,
        )

    grant = issue_trusted_sso_grant(request.user, client_id, redirect_uri)
    redirect_params = {"code": str(grant.public_id)}
    if state:
        redirect_params["state"] = state
    return redirect(f"{redirect_uri}?{urlencode(redirect_params)}")


@csrf_exempt
def sso_token(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        payload = _parse_json_body(request)
        identity_payload = exchange_trusted_sso_grant(
            payload.get("client_id"),
            payload.get("client_secret"),
            payload.get("code"),
            payload.get("redirect_uri"),
        )
    except AuthFlowError as exc:
        return _error_response(exc)

    return JsonResponse(identity_payload)
