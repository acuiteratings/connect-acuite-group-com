import json
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from directory.models import DirectoryProfile
from operations.services import record_analytics_event, record_audit_event

from .models import User
from .session import ensure_session_deadline
from .serializers import serialize_user
from .services import (
    AuthFlowError,
    SESSION_AUTH_BACKEND,
    change_password_after_challenge,
    complete_login,
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
        "mode": "manual_accounts_with_email_otp_and_password",
        "password_max_age_days": settings.AUTH_PASSWORD_MAX_AGE_DAYS,
        "otp_ttl_minutes": settings.AUTH_OTP_TTL_MINUTES,
        "otp_code_length": settings.AUTH_OTP_CODE_LENGTH,
        "account_provisioning": "manual_admin_control",
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


def _authenticated_payload(request, *, password_changed=False):
    permissions = sorted(request.user.get_all_permissions())
    session_deadline = ensure_session_deadline(request)
    return {
        "authenticated": True,
        "user": serialize_user(request.user),
        "permissions": permissions,
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
            "next_auth_decision": [
                "manual_employee_account",
                "email_otp",
                "password_with_rotation",
            ],
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
    return JsonResponse({"authenticated": False, "detail": "Logged out successfully."})


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
