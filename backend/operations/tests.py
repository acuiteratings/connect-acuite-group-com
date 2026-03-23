import json

from django.test import TestCase, override_settings

from accounts.models import User
from feed.models import Comment, Post

from .models import AnalyticsEvent, AuditLog, ErrorEvent


class OperationsApiTests(TestCase):
    def setUp(self):
        self.staff = User.objects.create_user(
            email="moderator@acuite.in",
            password="testpass123",
            first_name="Mod",
            last_name="Erator",
            title="Internal Comms",
            department="HR",
            is_staff=True,
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

    def test_moderation_queue_returns_pending_items_for_staff(self):
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
