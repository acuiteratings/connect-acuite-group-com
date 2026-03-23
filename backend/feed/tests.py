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
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(AuditLog.objects.filter(action="post.created").count(), 1)
        self.assertEqual(AnalyticsEvent.objects.filter(event_name="post_created").count(), 1)
