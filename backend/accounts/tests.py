import re
from datetime import timedelta
from urllib.parse import parse_qs, urlparse

from django.core import mail
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from django.utils import timezone

from directory.models import DirectoryProfile
from feed.models import Comment, Post
from operations.models import AnalyticsEvent, AuditLog, ErrorEvent

from .models import LoginChallenge, TrustedAppLoginGrant, User


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    AUTH_DEBUG_OTP_PREVIEW=False,
)
class AuthApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="employee.one@acuite.in",
            password="Welcome@123",
            first_name="Employee",
            last_name="One",
            must_change_password=False,
            password_changed_at=timezone.now(),
        )

    def test_me_endpoint_returns_unauthenticated_payload_for_anonymous_request(self):
        response = self.client.get("/api/accounts/me/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertFalse(payload["authenticated"])
        self.assertEqual(payload["auth_policy"]["mode"], "manual_accounts_with_email_otp_and_password")

    def test_request_otp_creates_challenge_and_sends_email(self):
        response = self.client.post(
            "/api/accounts/auth/request-otp/",
            data={"email": self.user.email},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertIn("challenge_token", payload)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(LoginChallenge.objects.count(), 1)

    def test_forgot_password_emails_first_time_password_and_forces_change(self):
        response = self.client.post(
            "/api/accounts/auth/forgot-password/",
            data={"email": self.user.email},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("314159", mail.outbox[0].body)

        self.user.refresh_from_db()
        self.assertTrue(self.user.must_change_password)
        self.assertIsNone(self.user.password_changed_at)
        self.assertTrue(self.user.check_password("314159"))

    def test_forgot_password_returns_generic_success_for_unknown_email(self):
        response = self.client.post(
            "/api/accounts/auth/forgot-password/",
            data={"email": "unknown.user@acuite.in"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["detail"],
            "If the email is provisioned, the temporary password has been emailed. Request a fresh OTP, then log in and change your password.",
        )
        self.assertEqual(len(mail.outbox), 0)

    def test_full_login_flow_requires_validated_otp_before_password(self):
        otp_response = self.client.post(
            "/api/accounts/auth/request-otp/",
            data={"email": self.user.email},
            content_type="application/json",
        )
        challenge_token = otp_response.json()["challenge_token"]
        otp = self._otp_from_mail()

        verify_response = self.client.post(
            "/api/accounts/auth/verify-otp/",
            data={"challenge_token": challenge_token, "otp": otp},
            content_type="application/json",
        )
        self.assertEqual(verify_response.status_code, 200)

        login_response = self.client.post(
            "/api/accounts/auth/login/",
            data={"challenge_token": challenge_token, "password": "Welcome@123"},
            content_type="application/json",
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(login_response.json()["authenticated"])

        me_response = self.client.get("/api/accounts/me/")
        self.assertEqual(me_response.status_code, 200)
        self.assertTrue(me_response.json()["authenticated"])

    def test_first_login_forces_password_change_before_session_is_created(self):
        first_login_user = User.objects.create_user(
            email="first.login@acuite.in",
            password="TempPass@123",
            must_change_password=True,
            password_changed_at=None,
        )

        otp_response = self.client.post(
            "/api/accounts/auth/request-otp/",
            data={"email": first_login_user.email},
            content_type="application/json",
        )
        challenge_token = otp_response.json()["challenge_token"]
        otp = self._otp_from_mail()
        self.client.post(
            "/api/accounts/auth/verify-otp/",
            data={"challenge_token": challenge_token, "otp": otp},
            content_type="application/json",
        )

        login_response = self.client.post(
            "/api/accounts/auth/login/",
            data={"challenge_token": challenge_token, "password": "TempPass@123"},
            content_type="application/json",
        )
        self.assertEqual(login_response.status_code, 200)
        payload = login_response.json()
        self.assertTrue(payload["requires_password_change"])
        self.assertEqual(payload["reason"], "first_login")

        change_response = self.client.post(
            "/api/accounts/auth/change-password/",
            data={
                "challenge_token": challenge_token,
                "new_password": "FreshPass@456",
                "confirm_password": "FreshPass@456",
            },
            content_type="application/json",
        )
        self.assertEqual(change_response.status_code, 200)
        self.assertTrue(change_response.json()["authenticated"])

        first_login_user.refresh_from_db()
        self.assertFalse(first_login_user.must_change_password)
        self.assertIsNotNone(first_login_user.password_changed_at)
        self.assertTrue(first_login_user.check_password("FreshPass@456"))

    def test_expired_password_requires_change(self):
        self.user.password_changed_at = timezone.now() - timedelta(days=120)
        self.user.must_change_password = False
        self.user.save(update_fields=["password_changed_at", "must_change_password", "updated_at"])

        otp_response = self.client.post(
            "/api/accounts/auth/request-otp/",
            data={"email": self.user.email},
            content_type="application/json",
        )
        challenge_token = otp_response.json()["challenge_token"]
        otp = self._otp_from_mail()

        self.client.post(
            "/api/accounts/auth/verify-otp/",
            data={"challenge_token": challenge_token, "otp": otp},
            content_type="application/json",
        )
        login_response = self.client.post(
            "/api/accounts/auth/login/",
            data={"challenge_token": challenge_token, "password": "Welcome@123"},
            content_type="application/json",
        )

        self.assertEqual(login_response.status_code, 200)
        self.assertTrue(login_response.json()["requires_password_change"])
        self.assertEqual(login_response.json()["reason"], "expired")

    def test_logout_endpoint_clears_authenticated_session(self):
        otp_response = self.client.post(
            "/api/accounts/auth/request-otp/",
            data={"email": self.user.email},
            content_type="application/json",
        )
        challenge_token = otp_response.json()["challenge_token"]
        otp = self._otp_from_mail()

        self.client.post(
            "/api/accounts/auth/verify-otp/",
            data={"challenge_token": challenge_token, "otp": otp},
            content_type="application/json",
        )
        self.client.post(
            "/api/accounts/auth/login/",
            data={"challenge_token": challenge_token, "password": "Welcome@123"},
            content_type="application/json",
        )

        logout_response = self.client.post("/api/accounts/auth/logout/")
        self.assertEqual(logout_response.status_code, 200)
        self.assertFalse(logout_response.json()["authenticated"])

        me_response = self.client.get("/api/accounts/me/")
        self.assertFalse(me_response.json()["authenticated"])

    @override_settings(
        TRUSTED_SSO_CLIENTS={
            "karma": {
                "client_secret": "shared-secret",
                "redirect_uris": ["https://karma.example.com/accounts/connect/callback/"],
            }
        }
    )
    def test_sso_authorize_redirects_anonymous_user_to_login_page_with_next(self):
        response = self.client.get(
            "/api/accounts/auth/sso/authorize/",
            {
                "client_id": "karma",
                "redirect_uri": "https://karma.example.com/accounts/connect/callback/",
                "state": "state-123",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login.html?next=", response["Location"])

    @override_settings(
        TRUSTED_SSO_CLIENTS={
            "karma": {
                "client_secret": "shared-secret",
                "redirect_uris": ["https://karma.example.com/accounts/connect/callback/"],
            }
        }
    )
    def test_sso_authorize_and_token_exchange_return_identity_payload(self):
        self.client.force_login(self.user)

        authorize_response = self.client.get(
            "/api/accounts/auth/sso/authorize/",
            {
                "client_id": "karma",
                "redirect_uri": "https://karma.example.com/accounts/connect/callback/",
                "state": "state-123",
            },
        )

        self.assertEqual(authorize_response.status_code, 302)
        redirect_url = urlparse(authorize_response["Location"])
        self.assertEqual(
            f"{redirect_url.scheme}://{redirect_url.netloc}{redirect_url.path}",
            "https://karma.example.com/accounts/connect/callback/",
        )
        redirect_params = parse_qs(redirect_url.query)
        self.assertEqual(redirect_params["state"], ["state-123"])
        grant_code = redirect_params["code"][0]
        self.assertTrue(TrustedAppLoginGrant.objects.filter(public_id=grant_code).exists())

        token_response = self.client.post(
            "/api/accounts/auth/sso/token/",
            data={
                "client_id": "karma",
                "client_secret": "shared-secret",
                "redirect_uri": "https://karma.example.com/accounts/connect/callback/",
                "code": grant_code,
            },
            content_type="application/json",
        )

        self.assertEqual(token_response.status_code, 200)
        self.assertEqual(token_response.json()["email"], self.user.email)
        grant = TrustedAppLoginGrant.objects.get(public_id=grant_code)
        self.assertIsNotNone(grant.consumed_at)

    def _otp_from_mail(self):
        body = mail.outbox[-1].body
        match = re.search(r"(\d{6})", body)
        self.assertIsNotNone(match)
        return match.group(1)


class RemoveEmployeeAccountCommandTests(TestCase):
    def test_remove_employee_account_deletes_related_employee_data(self):
        user = User.objects.create_user(
            email="notapplicable@notvalid.in",
            password="314159",
            display_name="Placeholder User",
        )
        DirectoryProfile.objects.create(user=user, company_name="Acuite", office_location="Mumbai")
        post = Post.objects.create(
            author=user,
            title="Placeholder post",
            body="Body",
            moderation_status=Post.ModerationStatus.PUBLISHED,
        )
        Comment.objects.create(author=user, post=post, body="Placeholder comment")
        LoginChallenge.objects.create(
            user=user,
            email=user.email,
            code_hash="hash",
            expires_at=timezone.now() + timedelta(minutes=10),
        )
        TrustedAppLoginGrant.objects.create(
            user=user,
            client_id="karma",
            redirect_uri="https://karma.example.com/accounts/connect/callback/",
            expires_at=timezone.now() + timedelta(minutes=10),
        )
        AnalyticsEvent.objects.create(actor=user, category="auth", event_name="login")
        AuditLog.objects.create(actor=user, action="test", summary="test summary")
        ErrorEvent.objects.create(actor=user, exception_type="ValueError", message="boom")

        call_command("remove_employee_account", user.email)

        self.assertFalse(User.objects.filter(email=user.email).exists())
        self.assertFalse(DirectoryProfile.objects.filter(user_id=user.id).exists())
        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(LoginChallenge.objects.count(), 0)
        self.assertEqual(TrustedAppLoginGrant.objects.count(), 0)
        self.assertEqual(AnalyticsEvent.objects.count(), 0)
        self.assertEqual(AuditLog.objects.count(), 0)
        self.assertEqual(ErrorEvent.objects.count(), 0)

    def test_remove_employee_account_refuses_staff_user(self):
        staff_user = User.objects.create_user(
            email="admin@acuite.in",
            password="314159",
            is_staff=True,
        )

        with self.assertRaisesMessage(CommandError, "Refusing to delete privileged account"):
            call_command("remove_employee_account", staff_user.email)

        self.assertTrue(User.objects.filter(email=staff_user.email).exists())
