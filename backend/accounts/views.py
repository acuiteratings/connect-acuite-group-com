import json
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from operations.services import record_analytics_event, record_audit_event

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


def _password_change_reason(user):
    if user.must_change_password or not user.password_changed_at:
        return "first_login"
    return "expired"


def _authenticated_payload(request, *, password_changed=False):
    permissions = sorted(request.user.get_all_permissions())
    return {
        "authenticated": True,
        "user": serialize_user(request.user),
        "permissions": permissions,
        "password_changed": password_changed,
        "auth_policy": _auth_policy_payload(),
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
        "detail": f"OTP sent to {challenge.masked_email}.",
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
