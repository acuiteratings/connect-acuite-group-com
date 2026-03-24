import logging
import random
from datetime import timedelta
from secrets import compare_digest
from threading import Thread

from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import LoginChallenge, TrustedAppLoginGrant, User


SESSION_AUTH_BACKEND = "django.contrib.auth.backends.ModelBackend"
logger = logging.getLogger(__name__)


class AuthFlowError(Exception):
    def __init__(self, message, *, status=400, code="auth_error", extra=None):
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.extra = extra or {}


def normalize_email(email):
    return str(email or "").strip().lower()


def generate_otp_code():
    length = max(4, int(getattr(settings, "AUTH_OTP_CODE_LENGTH", 6)))
    return "".join(str(random.randint(0, 9)) for _ in range(length))


def get_login_user(email):
    normalized_email = normalize_email(email)
    if not normalized_email:
        raise AuthFlowError("Email is required.", status=400, code="email_required")

    try:
        validate_email(normalized_email)
    except ValidationError as exc:
        raise AuthFlowError("Enter a valid employee email ID.", status=400, code="email_invalid") from exc

    try:
        user = User.objects.get(email=normalized_email)
    except User.DoesNotExist as exc:
        raise AuthFlowError(
            "This email is not provisioned for Acuité Connect.",
            status=404,
            code="user_not_found",
        ) from exc

    if not user.login_allowed:
        raise AuthFlowError(
            "This account is not currently active for Acuité Connect.",
            status=403,
            code="user_inactive",
        )

    return user


def get_login_challenge(public_id):
    token = str(public_id or "").strip()
    if not token:
        raise AuthFlowError("Challenge token is required.", status=400, code="challenge_required")

    try:
        challenge = LoginChallenge.objects.select_related("user").get(public_id=token)
    except (ValueError, LoginChallenge.DoesNotExist) as exc:
        raise AuthFlowError("This login session is not valid anymore.", status=404, code="challenge_not_found") from exc

    if challenge.consumed_at:
        raise AuthFlowError("This login session has already been used.", status=409, code="challenge_consumed")
    if challenge.is_expired:
        raise AuthFlowError("This OTP has expired. Please request a new one.", status=410, code="challenge_expired")

    return challenge


def _email_delivery_configured():
    backend = getattr(settings, "EMAIL_BACKEND", "")
    if "console.EmailBackend" in backend or "locmem.EmailBackend" in backend:
        return True
    return bool(getattr(settings, "EMAIL_HOST", "").strip())


def _deliver_email_safely(send_fn, *args):
    try:
        send_fn(*args)
    except Exception:
        logger.exception("Email delivery failed for Acuite Connect auth flow.")


def _send_email(send_fn, *args):
    backend = getattr(settings, "EMAIL_BACKEND", "")
    if "smtp.EmailBackend" in backend:
        Thread(target=_deliver_email_safely, args=(send_fn, *args), daemon=True).start()
        return
    send_fn(*args)


def _send_login_otp_email(user, code):
    subject = "Your Acuite Connect login OTP"
    message = (
        f"Hello {user.full_name},\n\n"
        f"Your Acuite Connect one-time password is {code}.\n"
        f"It expires in {settings.AUTH_OTP_TTL_MINUTES} minutes.\n\n"
        "If you did not request this code, please ignore this email."
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def _send_first_time_password_email(user, temporary_password):
    subject = "Your Acuite Connect temporary password"
    message = (
        f"Hello {user.full_name},\n\n"
        "Your Acuite Connect password has been reset.\n"
        f"Temporary password: {temporary_password}\n\n"
        "Use this password to log in after requesting a fresh OTP.\n"
        "You will be asked to choose a new password immediately.\n\n"
        "If you did not request this reset, please contact the internal admin team."
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )


def start_login_challenge(email):
    user = get_login_user(email)
    now = timezone.now()
    cooldown_seconds = int(getattr(settings, "AUTH_OTP_RESEND_COOLDOWN_SECONDS", 60))
    latest = (
        LoginChallenge.objects.filter(user=user)
        .order_by("-otp_sent_at")
        .first()
    )
    if latest and (now - latest.otp_sent_at).total_seconds() < cooldown_seconds:
        wait_seconds = cooldown_seconds - int((now - latest.otp_sent_at).total_seconds())
        raise AuthFlowError(
            f"Please wait {max(1, wait_seconds)} seconds before requesting another OTP.",
            status=429,
            code="otp_rate_limited",
            extra={"wait_seconds": max(1, wait_seconds)},
        )

    LoginChallenge.objects.filter(
        user=user,
        consumed_at__isnull=True,
    ).update(consumed_at=now)

    code = generate_otp_code()
    challenge = LoginChallenge.objects.create(
        user=user,
        email=user.email,
        code_hash=make_password(code),
        expires_at=now + timedelta(minutes=settings.AUTH_OTP_TTL_MINUTES),
        otp_sent_at=now,
    )

    preview_code = None
    if _email_delivery_configured():
        _send_email(_send_login_otp_email, user, code)
    elif settings.AUTH_DEBUG_OTP_PREVIEW:
        preview_code = code
    else:
        challenge.delete()
        raise AuthFlowError(
            "OTP email delivery is not configured yet. Ask an administrator to finish email setup.",
            status=503,
            code="otp_delivery_unavailable",
        )

    return challenge, preview_code


def reset_password_to_first_time_password(email):
    normalized_email = normalize_email(email)
    if not normalized_email:
        raise AuthFlowError("Enter your employee email ID first.", status=400, code="email_required")

    try:
        validate_email(normalized_email)
    except ValidationError as exc:
        raise AuthFlowError("Enter a valid employee email ID.", status=400, code="email_invalid") from exc

    try:
        user = get_login_user(normalized_email)
    except AuthFlowError as exc:
        if exc.code in {"user_not_found", "user_inactive"}:
            return None
        raise

    if not _email_delivery_configured():
        raise AuthFlowError(
            "Password reset email delivery is not configured yet. Ask an administrator to finish email setup.",
            status=503,
            code="reset_delivery_unavailable",
        )

    temporary_password = str(getattr(settings, "AUTH_FIRST_TIME_PASSWORD", "314159")).strip()
    if not temporary_password:
        raise AuthFlowError(
            "Temporary password reset is not configured yet. Ask an administrator to finish setup.",
            status=503,
            code="reset_password_unavailable",
        )

    now = timezone.now()
    try:
        with transaction.atomic():
            LoginChallenge.objects.filter(
                user=user,
                consumed_at__isnull=True,
            ).update(consumed_at=now)
            user.set_password(temporary_password)
            user.must_change_password = True
            user.password_changed_at = None
            user.save(update_fields=["password", "must_change_password", "password_changed_at", "updated_at"])
            _send_email(_send_first_time_password_email, user, temporary_password)
    except Exception as exc:
        raise AuthFlowError(
            "We couldn't send the reset email right now. Please try again in a moment.",
            status=503,
            code="reset_email_failed",
        ) from exc

    return user


def verify_login_otp(public_id, code):
    challenge = get_login_challenge(public_id)
    max_attempts = int(getattr(settings, "AUTH_OTP_MAX_ATTEMPTS", 5))

    if challenge.otp_verified_at:
        return challenge

    challenge.otp_attempts += 1
    if challenge.otp_attempts > max_attempts:
        challenge.consumed_at = timezone.now()
        challenge.save(update_fields=["otp_attempts", "consumed_at", "updated_at"])
        raise AuthFlowError(
            "Too many incorrect OTP attempts. Please request a new code.",
            status=429,
            code="otp_attempts_exceeded",
        )

    if not check_password(str(code or "").strip(), challenge.code_hash):
        challenge.save(update_fields=["otp_attempts", "updated_at"])
        raise AuthFlowError("That OTP is not valid.", status=400, code="otp_invalid")

    challenge.otp_verified_at = timezone.now()
    challenge.save(update_fields=["otp_attempts", "otp_verified_at", "updated_at"])
    return challenge


def validate_password_step(public_id, password):
    challenge = get_login_challenge(public_id)
    if not challenge.otp_verified_at:
        raise AuthFlowError("Validate the OTP before entering your password.", status=400, code="otp_required")

    user = challenge.user
    if not user.login_allowed:
        challenge.consumed_at = timezone.now()
        challenge.save(update_fields=["consumed_at", "updated_at"])
        raise AuthFlowError(
            "This account is not currently active for Acuité Connect.",
            status=403,
            code="user_inactive",
        )

    max_attempts = int(getattr(settings, "AUTH_PASSWORD_MAX_ATTEMPTS", 5))
    challenge.password_attempts += 1
    if challenge.password_attempts > max_attempts:
        challenge.consumed_at = timezone.now()
        challenge.save(update_fields=["password_attempts", "consumed_at", "updated_at"])
        raise AuthFlowError(
            "Too many incorrect password attempts. Please request a new OTP.",
            status=429,
            code="password_attempts_exceeded",
        )

    if not user.check_password(str(password or "")):
        challenge.save(update_fields=["password_attempts", "updated_at"])
        raise AuthFlowError("Incorrect password.", status=400, code="password_invalid")

    challenge.password_verified_at = timezone.now()
    challenge.save(update_fields=["password_attempts", "password_verified_at", "updated_at"])
    return challenge


def change_password_after_challenge(public_id, new_password):
    challenge = get_login_challenge(public_id)
    if not challenge.otp_verified_at or not challenge.password_verified_at:
        raise AuthFlowError(
            "Validate the OTP and current password before choosing a new password.",
            status=400,
            code="password_change_not_ready",
        )

    user = challenge.user
    candidate_password = str(new_password or "")
    if not candidate_password:
        raise AuthFlowError("New password is required.", status=400, code="new_password_required")

    if user.check_password(candidate_password):
        raise AuthFlowError(
            "Choose a password that is different from your current password.",
            status=400,
            code="password_unchanged",
        )

    try:
        validate_password(candidate_password, user=user)
    except ValidationError as exc:
        raise AuthFlowError(
            " ".join(exc.messages),
            status=400,
            code="password_invalid",
            extra={"validation_messages": exc.messages},
        ) from exc

    now = timezone.now()
    user.set_password(candidate_password)
    user.must_change_password = False
    user.password_changed_at = now
    user.save(update_fields=["password", "must_change_password", "password_changed_at", "updated_at"])

    challenge.consumed_at = now
    challenge.save(update_fields=["consumed_at", "updated_at"])
    return user


def complete_login(public_id):
    challenge = get_login_challenge(public_id)
    if not challenge.otp_verified_at:
        raise AuthFlowError("Validate the OTP before logging in.", status=400, code="otp_required")
    if challenge.user.password_change_required:
        raise AuthFlowError(
            "Password change required before login can complete.",
            status=409,
            code="password_change_required",
        )
    challenge.consumed_at = timezone.now()
    challenge.save(update_fields=["consumed_at", "updated_at"])
    return challenge.user


def get_trusted_sso_client(client_id):
    normalized_client_id = str(client_id or "").strip()
    if not normalized_client_id:
        raise AuthFlowError("Client ID is required.", status=400, code="client_required")

    clients = getattr(settings, "TRUSTED_SSO_CLIENTS", {})
    client = clients.get(normalized_client_id)
    if not client:
        raise AuthFlowError("This SSO client is not allowed.", status=403, code="client_not_allowed")
    return normalized_client_id, client


def validate_trusted_redirect_uri(client, redirect_uri):
    normalized_redirect_uri = str(redirect_uri or "").strip()
    if not normalized_redirect_uri:
        raise AuthFlowError("Redirect URI is required.", status=400, code="redirect_uri_required")
    if normalized_redirect_uri not in client.get("redirect_uris", []):
        raise AuthFlowError(
            "This redirect URI is not allowed for the client.",
            status=403,
            code="redirect_uri_not_allowed",
        )
    return normalized_redirect_uri


def issue_trusted_sso_grant(user, client_id, redirect_uri):
    TrustedAppLoginGrant.objects.filter(
        user=user,
        client_id=client_id,
        redirect_uri=redirect_uri,
        consumed_at__isnull=True,
    ).update(consumed_at=timezone.now())
    return TrustedAppLoginGrant.objects.create(
        user=user,
        client_id=client_id,
        redirect_uri=redirect_uri,
        expires_at=timezone.now()
        + timedelta(seconds=getattr(settings, "TRUSTED_SSO_CODE_TTL_SECONDS", 120)),
    )


def exchange_trusted_sso_grant(client_id, client_secret, code, redirect_uri):
    normalized_client_id, client = get_trusted_sso_client(client_id)
    normalized_redirect_uri = validate_trusted_redirect_uri(client, redirect_uri)
    expected_secret = str(client.get("client_secret", "")).strip()
    if not expected_secret or not compare_digest(expected_secret, str(client_secret or "").strip()):
        raise AuthFlowError("Client authentication failed.", status=403, code="client_auth_failed")

    token = str(code or "").strip()
    if not token:
        raise AuthFlowError("Code is required.", status=400, code="code_required")

    try:
        grant = TrustedAppLoginGrant.objects.select_related("user").get(public_id=token)
    except (ValueError, TrustedAppLoginGrant.DoesNotExist) as exc:
        raise AuthFlowError("This login handoff code is not valid.", status=404, code="grant_not_found") from exc

    if grant.consumed_at:
        raise AuthFlowError("This login handoff code has already been used.", status=409, code="grant_used")
    if grant.is_expired:
        raise AuthFlowError("This login handoff code has expired.", status=410, code="grant_expired")
    if grant.client_id != normalized_client_id:
        raise AuthFlowError("This login handoff code does not belong to the client.", status=403, code="grant_client_mismatch")
    if grant.redirect_uri != normalized_redirect_uri:
        raise AuthFlowError(
            "This login handoff code does not match the redirect URI.",
            status=403,
            code="grant_redirect_mismatch",
        )
    if not grant.user.login_allowed:
        grant.consumed_at = timezone.now()
        grant.save(update_fields=["consumed_at"])
        raise AuthFlowError(
            "This account is not currently active for Acuité Connect.",
            status=403,
            code="user_inactive",
        )

    grant.consumed_at = timezone.now()
    grant.save(update_fields=["consumed_at"])
    return {
        "email": grant.user.email,
        "first_name": grant.user.first_name,
        "last_name": grant.user.last_name,
        "display_name": grant.user.display_name or grant.user.full_name,
        "department": grant.user.department,
        "title": grant.user.title,
    }
