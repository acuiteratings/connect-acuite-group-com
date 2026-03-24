import json
import os
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase, override_settings

from accounts.models import User
from feed.models import Comment, Post

from .builds import get_current_build_number
from .models import AnalyticsEvent, AuditLog, BuildState, ErrorEvent


class OperationsApiTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            email="moderator@acuite.in",
            password="testpass123",
            first_name="Mod",
            last_name="Erator",
            title="Internal Comms",
            department="HR",
            access_level=User.AccessLevel.MODERATOR,
        )
        self.employee = User.objects.create_user(
            email="employee@acuite.in",
            password="testpass123",
            first_name="Sample",
            last_name="Employee",
            title="Analyst",
            department="Ratings",
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
        self.assertContains(response, "Built with care by Sankar Chakraborti | BUILD 1.0000007")

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
