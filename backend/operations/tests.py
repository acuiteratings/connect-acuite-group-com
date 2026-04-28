import json
import os
from io import StringIO
from datetime import date
from datetime import timedelta
from unittest.mock import patch

from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.utils import timezone

from accounts.models import User
from directory.models import DirectoryProfile
from feed.models import Comment, Post, PostReaction

from .builds import get_current_build_number
from .celebrations import publish_daily_celebration_posts
from .models import AnalyticsEvent, AuditLog, BuildState, ErrorEvent, ReportedError


class OperationsApiTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            email="moderator@acuite.in",
            password="testpass123",
            first_name="Mod",
            last_name="Erator",
            title="Internal Comms",
            department="HR",
            employee_code="MOD001",
            access_level=User.AccessLevel.MODERATOR,
        )
        self.admin = User.objects.create_user(
            email="admin@acuite.in",
            password="testpass123",
            first_name="Admin",
            last_name="User",
            title="Operations",
            department="HR",
            employee_code="ADM001",
            access_level=User.AccessLevel.ADMIN,
        )
        self.employee = User.objects.create_user(
            email="employee@acuite.in",
            password="testpass123",
            first_name="Sample",
            last_name="Employee",
            title="Analyst",
            department="Ratings",
            employee_code="EMP001",
        )
        self.pending_post = Post.objects.create(
            author=self.employee,
            title="Awaiting approval",
            body="Please review this before publish.",
            moderation_status=Post.ModerationStatus.PENDING_REVIEW,
        )
        self.pending_comment = Comment.objects.create(
            post=self.pending_post,
            author=self.employee,
            body="Pending note for moderation.",
            moderation_status=Comment.ModerationStatus.PENDING_REVIEW,
        )

    def test_ops_summary_requires_moderation_access(self):
        response = self.client.get("/api/ops/summary/")

        self.assertEqual(response.status_code, 403)

    def test_moderation_queue_returns_pending_items_for_moderator_access(self):
        self.client.force_login(self.staff)

        response = self.client.get("/api/ops/moderation/queue/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["counts"]["pending_posts"], 1)
        self.assertEqual(payload["counts"]["pending_comments"], 1)
        self.assertEqual(payload["posts"][0]["title"], "Awaiting approval")

    def test_moderating_post_writes_audit_and_analytics(self):
        self.client.force_login(self.staff)

        response = self.client.post(
            f"/api/ops/moderation/posts/{self.pending_post.id}/decision/",
            data=json.dumps({"decision": "publish", "note": "Looks good"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.pending_post.refresh_from_db()
        self.assertEqual(self.pending_post.moderation_status, Post.ModerationStatus.PUBLISHED)
        self.assertEqual(AuditLog.objects.filter(action="moderation.post.publish").count(), 1)
        self.assertEqual(AnalyticsEvent.objects.filter(event_name="post_publish").count(), 1)

    def test_analytics_ingest_records_event_and_request_id(self):
        self.client.force_login(self.employee)

        response = self.client.post(
            "/api/ops/analytics/ingest/",
            data=json.dumps(
                {
                    "category": "ui",
                    "event_name": "directory_opened",
                    "path": "/directory",
                    "metadata": {"source": "navigation"},
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(response["X-Request-ID"])
        self.assertEqual(AnalyticsEvent.objects.filter(event_name="directory_opened").count(), 1)

    def test_authenticated_employee_can_report_an_error(self):
        self.client.force_login(self.employee)

        response = self.client.post(
            "/api/ops/reported-errors/",
            data=json.dumps(
                {
                    "title": "Bulletin Board is blank",
                    "details": "The Bulletin Board stayed empty after refresh.",
                    "source_tab": "bulletin",
                    "page_path": "/index.html",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(ReportedError.objects.count(), 1)
        reported_error = ReportedError.objects.get()
        self.assertEqual(reported_error.reporter, self.employee)
        self.assertEqual(reported_error.source_tab, "bulletin")

    def test_engagement_score_overview_requires_admin_access(self):
        self.client.force_login(self.staff)

        response = self.client.get("/api/ops/engagement-score/")

        self.assertEqual(response.status_code, 403)

    def test_only_admin_can_list_and_delete_reported_errors(self):
        ReportedError.objects.create(
            reporter=self.employee,
            title="Directory filter issue",
            details="Location chips are wrong.",
            source_tab="directory",
        )
        self.client.force_login(self.employee)

        employee_response = self.client.get("/api/ops/reported-errors/")
        self.assertEqual(employee_response.status_code, 403)

        self.client.force_login(self.staff)
        list_response = self.client.get("/api/ops/reported-errors/")
        self.assertEqual(list_response.status_code, 403)

        self.client.force_login(self.admin)
        admin_list_response = self.client.get("/api/ops/reported-errors/")
        self.assertEqual(admin_list_response.status_code, 200)
        payload = admin_list_response.json()
        self.assertEqual(payload["count"], 1)

        reported_error_id = payload["results"][0]["id"]
        delete_response = self.client.delete(f"/api/ops/reported-errors/{reported_error_id}/")
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(ReportedError.objects.count(), 0)

    def test_engagement_score_overview_returns_counts_and_scores_for_admin(self):
        quiet_user = User.objects.create_user(
            email="quiet@acuite.in",
            password="testpass123",
            first_name="Quiet",
            last_name="User",
            title="Associate",
            department="Ratings",
            employee_code="EMP002",
        )
        liked_post_one = Post.objects.create(
            author=self.staff,
            title="Liked once",
            body="Published content",
            moderation_status=Post.ModerationStatus.PUBLISHED,
            published_at=timezone.now(),
        )
        liked_post_two = Post.objects.create(
            author=self.admin,
            title="Liked twice",
            body="Published content",
            moderation_status=Post.ModerationStatus.PUBLISHED,
            published_at=timezone.now(),
        )
        Post.objects.create(
            author=self.employee,
            title="My first live post",
            body="Published employee message",
            moderation_status=Post.ModerationStatus.PUBLISHED,
            published_at=timezone.now(),
        )
        Post.objects.create(
            author=self.employee,
            title="My second live post",
            body="Another published employee message",
            moderation_status=Post.ModerationStatus.PUBLISHED,
            published_at=timezone.now(),
        )
        PostReaction.objects.create(post=liked_post_one, user=self.employee)
        PostReaction.objects.create(post=liked_post_two, user=self.employee)
        Comment.objects.create(
            post=liked_post_one,
            author=self.employee,
            body="Thoughtful comment",
            moderation_status=Comment.ModerationStatus.PUBLISHED,
        )
        AnalyticsEvent.objects.create(actor=self.employee, category="auth", event_name="login_completed")
        AnalyticsEvent.objects.create(actor=self.employee, category="auth", event_name="employee_sso_login_completed")
        AnalyticsEvent.objects.create(actor=self.employee, category="auth", event_name="password_changed_during_login")
        AnalyticsEvent.objects.create(actor=self.employee, category="auth", event_name="logout_completed")
        AnalyticsEvent.objects.create(actor=quiet_user, category="auth", event_name="login_completed")

        self.client.force_login(self.admin)

        response = self.client.get("/api/ops/engagement-score/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        rows = {row["employee_name"]: row for row in payload["results"]}
        employee_row = rows[self.employee.full_name]
        quiet_row = rows[quiet_user.full_name]

        self.assertEqual(employee_row["employee_code"], "EMP001")
        self.assertEqual(employee_row["likes_given"], 2)
        self.assertEqual(employee_row["comments_given"], 1)
        self.assertEqual(employee_row["logins_done"], 3)
        self.assertEqual(employee_row["messages_posted"], 2)
        self.assertEqual(employee_row["engagement_score"], 10.0)
        self.assertEqual(quiet_row["employee_code"], "EMP002")
        self.assertEqual(quiet_row["likes_given"], 0)
        self.assertEqual(quiet_row["comments_given"], 0)
        self.assertEqual(quiet_row["logins_done"], 1)
        self.assertEqual(quiet_row["messages_posted"], 0)
        self.assertLess(quiet_row["engagement_score"], employee_row["engagement_score"])
        self.assertEqual(payload["results"][0]["employee_name"], self.employee.full_name)
        self.assertEqual(payload["formula"]["scale"], "0-10")


class SecurityHeadersMiddlewareTests(TestCase):
    def test_html_shells_include_security_headers_and_no_store_cache_policy(self):
        response = self.client.get("/login.html")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Security-Policy"], settings.CONTENT_SECURITY_POLICY)
        self.assertEqual(response["Permissions-Policy"], settings.PERMISSIONS_POLICY)
        self.assertEqual(
            response["Cache-Control"],
            "no-store, no-cache, must-revalidate, max-age=0",
        )
        self.assertEqual(response["Pragma"], "no-cache")
        self.assertEqual(response["Expires"], "0")

    def test_api_responses_include_security_headers_and_no_store_cache_policy(self):
        response = self.client.get("/api/accounts/me/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Security-Policy"], settings.CONTENT_SECURITY_POLICY)
        self.assertEqual(response["Permissions-Policy"], settings.PERMISSIONS_POLICY)
        self.assertEqual(
            response["Cache-Control"],
            "no-store, no-cache, must-revalidate, max-age=0",
        )
        self.assertEqual(response["Pragma"], "no-cache")
        self.assertEqual(response["Expires"], "0")


@override_settings(ROOT_URLCONF="operations.test_urls")
class ErrorMonitoringMiddlewareTests(TestCase):
    def test_unhandled_exception_is_recorded(self):
        self.client.raise_request_exception = False

        response = self.client.get("/boom/")

        self.assertEqual(response.status_code, 500)
        self.assertEqual(ErrorEvent.objects.count(), 1)
        error_event = ErrorEvent.objects.get()
        self.assertEqual(error_event.exception_type, "RuntimeError")
        self.assertEqual(error_event.path, "/boom/")


class BuildNumberTests(TestCase):
    def test_login_page_uses_registered_build_number(self):
        BuildState.objects.create(counter=7, display_number="1.0000007")

        response = self.client.get("/login.html")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "BUILD 1.0000007")

    @override_settings(APP_BUILD_NUMBER="1.0000006")
    def test_build_number_falls_back_to_settings_when_state_missing(self):
        self.assertEqual(get_current_build_number(), "1.0000006")

    @patch.dict(os.environ, {"APP_BUILD_COUNTER_SEED": "6", "RENDER_GIT_COMMIT": "abc123"})
    def test_register_build_command_increments_database_counter(self):
        call_command("register_build_deploy")

        state = BuildState.objects.get(singleton_key="primary")
        self.assertEqual(state.counter, 7)
        self.assertEqual(state.display_number, "1.0000007")
        self.assertEqual(state.commit_sha, "abc123")

    def test_healthcheck_exposes_build_and_commit_for_smoke_checks(self):
        BuildState.objects.create(
            counter=8,
            display_number="1.0000008",
            commit_sha="deadbeef123456",
        )

        response = self.client.get("/api/ops/health/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["build_number"], "1.0000008")
        self.assertEqual(payload["commit_sha"], "deadbeef123456")


class ClearLiveDemoDataCommandTests(TestCase):
    def test_clear_live_demo_data_removes_operational_demo_records(self):
        user = User.objects.create_user(
            email="tester@acuite.in",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        post = Post.objects.create(
            author=user,
            title="Seeded demo post",
            body="Demo body",
        )
        Comment.objects.create(
            post=post,
            author=user,
            body="Demo comment",
        )
        AuditLog.objects.create(
            actor=user,
            action="demo.seed",
            summary="Seeded audit",
        )
        AnalyticsEvent.objects.create(
            actor=user,
            category="demo",
            event_name="seeded",
        )
        ErrorEvent.objects.create(
            actor=user,
            exception_type="RuntimeError",
            message="Seeded error",
        )

        call_command("clear_live_demo_data")

        self.assertEqual(Post.objects.count(), 0)
        self.assertEqual(Comment.objects.count(), 0)
        self.assertEqual(AuditLog.objects.count(), 0)
        self.assertEqual(AnalyticsEvent.objects.count(), 0)
        self.assertEqual(ErrorEvent.objects.count(), 0)


class PruneOperationalEventsCommandTests(TestCase):
    def test_prune_operational_events_removes_records_past_retention_windows(self):
        user = User.objects.create_user(
            email="ops.retention@acuite.in",
            password="testpass123",
            first_name="Ops",
            last_name="Retention",
        )
        now = timezone.now()
        old_analytics = AnalyticsEvent.objects.create(
            actor=user,
            category="ui",
            event_name="old_click",
        )
        recent_analytics = AnalyticsEvent.objects.create(
            actor=user,
            category="ui",
            event_name="recent_click",
        )
        old_audit = AuditLog.objects.create(actor=user, action="old.audit", summary="Old audit")
        recent_audit = AuditLog.objects.create(actor=user, action="recent.audit", summary="Recent audit")
        old_resolved_error = ErrorEvent.objects.create(
            actor=user,
            exception_type="RuntimeError",
            message="Old resolved",
            is_resolved=True,
            resolved_at=now - timedelta(days=120),
        )
        recent_resolved_error = ErrorEvent.objects.create(
            actor=user,
            exception_type="RuntimeError",
            message="Recent resolved",
            is_resolved=True,
            resolved_at=now - timedelta(days=10),
        )
        old_report = ReportedError.objects.create(
            reporter=user,
            title="Old resolved report",
            details="Old details",
            is_resolved=True,
            resolved_at=now - timedelta(days=220),
        )
        recent_report = ReportedError.objects.create(
            reporter=user,
            title="Recent report",
            details="Recent details",
        )
        AnalyticsEvent.objects.filter(pk=old_analytics.pk).update(
            occurred_at=now - timedelta(days=220)
        )
        AnalyticsEvent.objects.filter(pk=recent_analytics.pk).update(
            occurred_at=now - timedelta(days=10)
        )
        AuditLog.objects.filter(pk=old_audit.pk).update(created_at=now - timedelta(days=400))
        AuditLog.objects.filter(pk=recent_audit.pk).update(created_at=now - timedelta(days=10))
        ErrorEvent.objects.filter(pk=old_resolved_error.pk).update(
            occurred_at=now - timedelta(days=120)
        )
        ErrorEvent.objects.filter(pk=recent_resolved_error.pk).update(
            occurred_at=now - timedelta(days=10)
        )
        ReportedError.objects.filter(pk=old_report.pk).update(
            created_at=now - timedelta(days=220)
        )
        ReportedError.objects.filter(pk=recent_report.pk).update(
            created_at=now - timedelta(days=10)
        )

        output = StringIO()
        call_command("prune_operational_events", stdout=output)

        self.assertFalse(AnalyticsEvent.objects.filter(pk=old_analytics.pk).exists())
        self.assertTrue(AnalyticsEvent.objects.filter(pk=recent_analytics.pk).exists())
        self.assertFalse(AuditLog.objects.filter(pk=old_audit.pk).exists())
        self.assertTrue(AuditLog.objects.filter(pk=recent_audit.pk).exists())
        self.assertFalse(ErrorEvent.objects.filter(pk=old_resolved_error.pk).exists())
        self.assertTrue(ErrorEvent.objects.filter(pk=recent_resolved_error.pk).exists())
        self.assertFalse(ReportedError.objects.filter(pk=old_report.pk).exists())
        self.assertTrue(ReportedError.objects.filter(pk=recent_report.pk).exists())
        self.assertIn("Pruned:", output.getvalue())


class DailyCelebrationPublishingTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@acuite.in",
            password="testpass123",
            first_name="Admin",
            last_name="User",
            access_level=User.AccessLevel.ADMIN,
            employment_status=User.EmploymentStatus.ACTIVE,
        )
        self.today = timezone.localdate()
        self.birthday_user = User.objects.create_user(
            email="birthday@acuite.in",
            password="testpass123",
            first_name="Priya",
            last_name="Sharma",
            department="Human Resource",
            employment_status=User.EmploymentStatus.ACTIVE,
        )
        DirectoryProfile.objects.create(
            user=self.birthday_user,
            date_of_birth=self.today,
            is_visible=True,
            profile_photos=["data:image/png;base64,AAAA"],
        )
        self.anniversary_user = User.objects.create_user(
            email="anniversary@acuite.in",
            password="testpass123",
            first_name="Aman",
            last_name="Patel",
            employment_status=User.EmploymentStatus.ACTIVE,
        )
        joined_on = date(self.today.year - 3, self.today.month, self.today.day)
        DirectoryProfile.objects.create(
            user=self.anniversary_user,
            joined_on=joined_on,
            is_visible=True,
            profile_photos=["https://example.com/photo.jpg"],
        )

    def test_publish_daily_celebration_posts_creates_birthday_and_anniversary_posts(self):
        result = publish_daily_celebration_posts(reference_date=self.today)

        self.assertEqual(len(result["created"]), 2)
        posts = list(Post.objects.order_by("title"))
        self.assertEqual(len(posts), 2)
        self.assertTrue(all(post.moderation_status == Post.ModerationStatus.PUBLISHED for post in posts))
        self.assertEqual(posts[0].metadata["bulletin_card"]["person_name"], posts[0].title.split(" | ")[-1])
        self.assertEqual(posts[0].metadata["bulletin_category"], "hr")
        self.assertEqual(AuditLog.objects.filter(action="post.auto_celebration.created").count(), 2)
        self.assertEqual(AnalyticsEvent.objects.filter(event_name="auto_celebration_post_created").count(), 2)

    def test_publish_daily_celebration_posts_is_idempotent_for_same_date(self):
        publish_daily_celebration_posts(reference_date=self.today)
        second_result = publish_daily_celebration_posts(reference_date=self.today)

        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(len(second_result["created"]), 0)
        self.assertEqual(len(second_result["skipped_existing"]), 2)


class CelebrationAdminApiTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@acuite.in",
            password="testpass123",
            first_name="Admin",
            last_name="User",
            access_level=User.AccessLevel.ADMIN,
            employment_status=User.EmploymentStatus.ACTIVE,
            is_staff=True,
        )
        self.today = timezone.localdate()
        self.birthday_user = User.objects.create_user(
            email="birthday@acuite.in",
            password="testpass123",
            first_name="Riya",
            last_name="Sen",
            department="Human Resource",
            employment_status=User.EmploymentStatus.ACTIVE,
        )
        DirectoryProfile.objects.create(
            user=self.birthday_user,
            date_of_birth=self.today,
            is_visible=True,
            profile_photos=["data:image/png;base64,AAAA"],
        )

    def test_celebration_today_requires_admin(self):
        response = self.client.get("/api/ops/celebrations/today/")

        self.assertEqual(response.status_code, 403)

    def test_celebration_today_lists_birthdays(self):
        self.client.force_login(self.admin)

        response = self.client.get("/api/ops/celebrations/today/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload["birthdays"]), 1)
        self.assertEqual(payload["birthdays"][0]["name"], "Riya Sen")

    def test_celebration_preview_returns_native_card_data(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            "/api/ops/celebrations/preview/",
            data=json.dumps({"kind": "birthday", "user_id": self.birthday_user.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()["preview"]
        self.assertEqual(payload["name"], "Riya Sen")
        self.assertEqual(payload["card"]["person_name"], "Riya Sen")
        self.assertEqual(payload["card"]["occasion_label"], "Happy Birthday")
        self.assertTrue(payload["template_file"].endswith(".html"))

    def test_celebration_preview_regenerate_rotates_template(self):
        self.client.force_login(self.admin)

        first_response = self.client.post(
            "/api/ops/celebrations/preview/",
            data=json.dumps({"kind": "birthday", "user_id": self.birthday_user.id}),
            content_type="application/json",
        )
        first_template = first_response.json()["preview"]["template_file"]

        second_response = self.client.post(
            "/api/ops/celebrations/preview/",
            data=json.dumps(
                {
                    "kind": "birthday",
                    "user_id": self.birthday_user.id,
                    "template_file": first_template,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(second_response.status_code, 200)
        self.assertNotEqual(second_response.json()["preview"]["template_file"], first_template)

    def test_celebration_publish_creates_post(self):
        self.client.force_login(self.admin)
        preview_response = self.client.post(
            "/api/ops/celebrations/preview/",
            data=json.dumps({"kind": "birthday", "user_id": self.birthday_user.id}),
            content_type="application/json",
        )
        template_file = preview_response.json()["preview"]["template_file"]

        response = self.client.post(
            "/api/ops/celebrations/publish/",
            data=json.dumps(
                {
                    "kind": "birthday",
                    "user_id": self.birthday_user.id,
                    "template_file": template_file,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.get()
        self.assertEqual(post.metadata["bulletin_card"]["person_name"], "Riya Sen")
        self.assertEqual(post.metadata["bulletin_template_file"], template_file)
