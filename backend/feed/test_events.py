import json

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from operations.models import OrgNotification

from .models import Post


class EventApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="employee.events@acuite.in",
            password="testpass123",
            first_name="Employee",
            last_name="Events",
        )
        self.admin_user = User.objects.create_user(
            email="admin.events@acuite.in",
            password="testpass123",
            first_name="Admin",
            last_name="Events",
            access_level=User.AccessLevel.ADMIN,
            must_change_password=False,
        )

    def test_admin_can_create_unpublished_event_with_external_links(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            "/api/feed/events/",
            data=json.dumps(
                {
                    "title": "Annual Awards",
                    "body": "Highlights from the annual awards evening.",
                    "moderation_status": Post.ModerationStatus.DRAFT,
                    "metadata": {
                        "event_date": "2026-05-05",
                        "event_media_links": [
                            {"label": "Open Album", "url": "https://drive.example.com/album"}
                        ],
                    },
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        post = Post.objects.get(topic="connect_events")
        self.assertEqual(post.module, Post.Module.BULLETIN)
        self.assertEqual(post.moderation_status, Post.ModerationStatus.DRAFT)
        self.assertIsNone(post.published_at)
        self.assertFalse(post.allow_comments)
        self.assertTrue(post.metadata["event_post"])
        self.assertEqual(post.metadata["event_media_links"][0]["label"], "Open Album")
        self.assertFalse(OrgNotification.objects.exists())

    def test_published_event_creates_org_notification(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            "/api/feed/events/",
            data=json.dumps(
                {
                    "title": "Townhall Photos",
                    "body": "Photos from the townhall are now available.",
                    "moderation_status": Post.ModerationStatus.PUBLISHED,
                    "metadata": {"event_date": "2026-06-15"},
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        notification = OrgNotification.objects.get()
        self.assertEqual(notification.category, OrgNotification.Category.EVENT)
        self.assertEqual(notification.target_tab, "home")
        self.assertEqual(notification.metadata["focus_sidebar"], "events")

    def test_employee_only_sees_published_events(self):
        published_post = Post.objects.create(
            author=self.admin_user,
            title="Published event",
            body="Visible event.",
            module=Post.Module.BULLETIN,
            topic="connect_events",
            moderation_status=Post.ModerationStatus.PUBLISHED,
            published_at=timezone.now(),
            metadata={"event_post": True},
        )
        Post.objects.create(
            author=self.admin_user,
            title="Unpublished event",
            body="Hidden event.",
            module=Post.Module.BULLETIN,
            topic="connect_events",
            moderation_status=Post.ModerationStatus.DRAFT,
            metadata={"event_post": True},
        )
        self.client.force_login(self.user)

        response = self.client.get("/api/feed/events/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["results"][0]["id"], published_post.id)

    def test_admin_can_update_unpublish_and_delete_event(self):
        post = Post.objects.create(
            author=self.admin_user,
            title="Old event",
            body="Old details.",
            module=Post.Module.BULLETIN,
            topic="connect_events",
            moderation_status=Post.ModerationStatus.PUBLISHED,
            published_at=timezone.now(),
            metadata={"event_post": True, "event_date": "2026-05-01"},
        )
        self.client.force_login(self.admin_user)

        update_response = self.client.patch(
            f"/api/feed/events/{post.id}/",
            data=json.dumps(
                {
                    "title": "Updated event",
                    "body": "Updated details.",
                    "metadata": {
                        "event_date": "2026-05-06",
                        "event_media_links": [
                            {"label": "Watch Video", "url": "https://video.example.com/watch"}
                        ],
                    },
                    "moderation_status": "draft",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(update_response.status_code, 200)
        post.refresh_from_db()
        self.assertEqual(post.title, "Updated event")
        self.assertEqual(post.moderation_status, Post.ModerationStatus.DRAFT)
        self.assertIsNone(post.published_at)
        self.assertEqual(post.metadata["event_date"], "2026-05-06")
        self.assertFalse(OrgNotification.objects.exists())

        delete_response = self.client.delete(f"/api/feed/events/{post.id}/")

        self.assertEqual(delete_response.status_code, 200)
        post.refresh_from_db()
        self.assertEqual(post.moderation_status, Post.ModerationStatus.REMOVED)
