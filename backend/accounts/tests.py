import json
import re
from datetime import datetime
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

from .models import ExitProcess, LoginChallenge, TrustedAppLoginGrant, User


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
        self.admin_user = User.objects.create_user(
            email="admin.one@acuite.in",
            password="Welcome@123",
            first_name="Admin",
            last_name="One",
            access_level=User.AccessLevel.ADMIN,
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
        challenge = LoginChallenge.objects.get()
        self.assertTrue(challenge.code_hash.startswith("hmac_sha256$"))
        self.assertRegex(mail.outbox[0].subject, r"Acuite Connect OTP: \d{6}")
        self.assertIn("font-size: 500%", mail.outbox[0].alternatives[0][0])

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

    def test_authenticated_session_includes_midnight_expiry(self):
        self.client.force_login(self.user)

        response = self.client.get("/api/accounts/me/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["authenticated"])
        self.assertIsNotNone(payload["session_expires_at"])

        deadline = datetime.fromisoformat(payload["session_expires_at"])
        local_deadline = timezone.localtime(deadline)
        self.assertEqual(local_deadline.hour, 0)
        self.assertEqual(local_deadline.minute, 0)

    def test_me_endpoint_returns_access_rights_for_authenticated_user(self):
        self.client.force_login(self.admin_user)

        response = self.client.get("/api/accounts/me/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(payload["authenticated"])
        self.assertEqual(payload["user"]["access_level"], User.AccessLevel.ADMIN)
        self.assertTrue(payload["user"]["access_rights"]["can_administer"])
        self.assertTrue(payload["user"]["access_rights"]["can_manage_access_rights"])
        self.assertTrue(payload["user"]["access_rights"]["can_post_as_company"])

    def test_admin_can_assign_access_rights_and_block_posting(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            f"/api/accounts/access/users/{self.user.id}/",
            data=json.dumps(
                {
                    "access_level": User.AccessLevel.MODERATOR,
                    "can_post_in_connect": False,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.access_level, User.AccessLevel.MODERATOR)
        self.assertFalse(self.user.can_post_in_connect)
        self.assertEqual(AuditLog.objects.filter(action="accounts.access.updated").count(), 1)

    def test_admin_can_create_employee_account(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            "/api/accounts/access/users/",
            data=json.dumps(
                {
                    "email": "new.employee@acuite.in",
                    "display_name": "New Employee",
                    "title": "Associate",
                    "department": "Technology",
                    "location": "Mumbai",
                    "access_level": User.AccessLevel.EMPLOYEE,
                    "can_post_in_connect": True,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        created = User.objects.get(email="new.employee@acuite.in")
        self.assertEqual(created.display_name, "New Employee")
        self.assertEqual(created.access_level, User.AccessLevel.EMPLOYEE)
        self.assertTrue(created.must_change_password)
        self.assertTrue(created.check_password("314159"))
        self.assertTrue(DirectoryProfile.objects.filter(user=created).exists())

    def test_admin_can_edit_employee_account_fields(self):
        self.client.force_login(self.admin_user)

        response = self.client.patch(
            f"/api/accounts/access/users/{self.user.id}/",
            data=json.dumps(
                {
                    "display_name": "Employee Prime",
                    "title": "Lead Analyst",
                    "location": "Ahmedabad",
                    "employment_status": User.EmploymentStatus.SUSPENDED,
                    "is_active": False,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.display_name, "Employee Prime")
        self.assertEqual(self.user.title, "Lead Analyst")
        self.assertEqual(self.user.location, "Ahmedabad")
        self.assertEqual(self.user.employment_status, User.EmploymentStatus.SUSPENDED)
        self.assertFalse(self.user.is_active)

    def test_admin_can_create_exit_process(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            "/api/accounts/access/exit-processes/",
            data=json.dumps(
                {
                    "employee_id": self.user.id,
                    "resignation_date": "2026-03-25",
                    "last_working_day": "2026-04-30",
                    "stage": "knowledge_transfer",
                    "resignation_acknowledged": True,
                    "knowledge_transfer_completed": False,
                    "assets_returned": False,
                    "access_review_completed": False,
                    "notes": "Manager accepted resignation.",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertEqual(payload["exit_process"]["employee"]["id"], self.user.id)
        self.assertEqual(payload["exit_process"]["stage"], "knowledge_transfer")
        self.assertEqual(payload["exit_process"]["notes"], "Manager accepted resignation.")
        self.assertEqual(ExitProcess.objects.count(), 1)

    def test_admin_can_finalize_exit_process_and_convert_employee_to_alumni(self):
        self.client.force_login(self.admin_user)
        DirectoryProfile.objects.create(
            user=self.user,
            company_name="Acuite",
            office_location="Mumbai",
            is_visible=True,
        )

        response = self.client.post(
            "/api/accounts/access/exit-processes/",
            data=json.dumps(
                {
                    "employee_id": self.user.id,
                    "resignation_date": "2026-03-25",
                    "last_working_day": "2026-04-30",
                    "stage": "completed",
                    "resignation_acknowledged": True,
                    "knowledge_transfer_completed": True,
                    "assets_returned": True,
                    "access_review_completed": True,
                    "notes": "All exit steps completed.",
                    "finalize": True,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.user.refresh_from_db()
        self.assertEqual(self.user.employment_status, User.EmploymentStatus.ALUMNI)
        self.assertFalse(self.user.is_active)
        self.assertFalse(self.user.can_post_in_connect)
        self.assertFalse(self.user.is_directory_visible)
        self.assertEqual(self.user.access_level, User.AccessLevel.EMPLOYEE)

        self.user.directory_profile.refresh_from_db()
        self.assertFalse(self.user.directory_profile.is_visible)

        process = ExitProcess.objects.get(employee=self.user)
        self.assertEqual(process.stage, ExitProcess.Stage.COMPLETED)
        self.assertTrue(process.alumni_transition_completed)
        self.assertIsNotNone(process.completed_at)

    def test_employee_cannot_assign_access_rights(self):
        self.client.force_login(self.user)

        response = self.client.get("/api/accounts/access/users/")

        self.assertEqual(response.status_code, 403)

    def test_expired_session_deadline_logs_user_out(self):
        self.client.force_login(self.user)
        session = self.client.session
        session["session_logout_at"] = (timezone.now() - timedelta(minutes=1)).isoformat()
        session.save()

        response = self.client.get("/api/accounts/me/")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["authenticated"])

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


class SetConnectAccessCommandTests(TestCase):
    def test_set_connect_access_promotes_user_and_enables_posting(self):
        user = User.objects.create_user(
            email="promote.me@acuite.in",
            password="314159",
            can_post_in_connect=False,
        )

        call_command(
            "set_connect_access",
            user.email,
            "--access-level",
            User.AccessLevel.ADMIN,
            "--enable-posting",
        )

        user.refresh_from_db()
        self.assertEqual(user.access_level, User.AccessLevel.ADMIN)
        self.assertTrue(user.can_post_in_connect)
