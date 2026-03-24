import json

from django.test import TestCase

from accounts.models import User
from operations.models import AnalyticsEvent, AuditLog

from .models import Post


class FeedApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="rahul.mehta@acuite.in",
            password="testpass123",
            first_name="Rahul",
            last_name="Mehta",
            title="Senior Analyst",
            department="Ratings",
        )

    def test_feed_lists_published_posts(self):
        Post.objects.create(
            author=self.user,
            title="Published post",
            body="Visible to everyone",
            moderation_status=Post.ModerationStatus.PUBLISHED,
        )
        Post.objects.create(
            author=self.user,
            title="Draft post",
            body="Hidden from anonymous users",
            moderation_status=Post.ModerationStatus.DRAFT,
        )

        response = self.client.get("/api/feed/posts/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["results"][0]["title"], "Published post")

    def test_authenticated_user_can_create_post(self):
        self.client.force_login(self.user)

        response = self.client.post(
            "/api/feed/posts/",
            data=json.dumps({"title": "Hello", "body": "First backend post"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertEqual(payload["post"]["title"], "Hello")
        self.assertEqual(payload["post"]["module"], Post.Module.GENERAL)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(AuditLog.objects.filter(action="post.created").count(), 1)
        self.assertEqual(AnalyticsEvent.objects.filter(event_name="post_created").count(), 1)

    def test_feed_can_filter_posts_by_module(self):
        Post.objects.create(
            author=self.user,
            title="Marketplace post",
            body="Selling a chair",
            module=Post.Module.COMMUNITY,
            topic="marketplace",
            moderation_status=Post.ModerationStatus.PUBLISHED,
        )
        Post.objects.create(
            author=self.user,
            title="Business note",
            body="Quarter close update",
            module=Post.Module.BUSINESS,
            topic="updates",
            moderation_status=Post.ModerationStatus.PUBLISHED,
        )

        response = self.client.get("/api/feed/posts/?module=community")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["results"][0]["title"], "Marketplace post")
        self.assertEqual(payload["results"][0]["topic"], "marketplace")

    def test_community_posts_auto_publish_for_authenticated_employee(self):
        self.client.force_login(self.user)

        response = self.client.post(
            "/api/feed/posts/",
            data=json.dumps(
                {
                    "title": "Need a flatmate in Mumbai",
                    "body": "Looking near Lower Parel from April.",
                    "module": "community",
                    "topic": "housing",
                    "metadata": {
                        "community_type": "looking_for_roommate",
                        "city": "Mumbai",
                        "meta_line": "Budget up to Rs 22,000",
                    },
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertEqual(payload["post"]["module"], "community")
        self.assertEqual(payload["post"]["topic"], "housing")
        self.assertEqual(
            payload["post"]["moderation_status"],
            Post.ModerationStatus.PUBLISHED,
        )
        self.assertEqual(payload["post"]["metadata"]["city"], "Mumbai")

    def test_ideas_voice_posts_auto_publish_for_authenticated_employee(self):
        self.client.force_login(self.user)

        response = self.client.post(
            "/api/feed/posts/",
            data=json.dumps(
                {
                    "title": "Idea for better sector sharing",
                    "body": "Create monthly cross-sector review circles.",
                    "module": "ideas_voice",
                    "topic": "idea",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.json()["post"]["moderation_status"],
            Post.ModerationStatus.PUBLISHED,
        )

    def test_ceo_corner_posts_require_staff_publish_access(self):
        self.client.force_login(self.user)

        response = self.client.post(
            "/api/feed/posts/",
            data=json.dumps(
                {
                    "title": "Leadership note",
                    "body": "A direct note to everyone.",
                    "module": "ideas_voice",
                    "topic": "ceo_corner",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Post.objects.count(), 0)
