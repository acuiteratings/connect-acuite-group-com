from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from directory.models import DirectoryProfile
from feed.models import Comment, Post, PostReaction


class RecognitionOverviewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="priya.sharma@acuite.in",
            password="testpass123",
            first_name="Priya",
            last_name="Sharma",
            title="Director - Financial Institutions",
            location="Mumbai",
        )
        self.peer = User.objects.create_user(
            email="karthik.iyer@acuite.in",
            password="testpass123",
            first_name="Karthik",
            last_name="Iyer",
            title="Associate Analyst",
            location="Bengaluru",
        )
        today = timezone.localdate()
        DirectoryProfile.objects.create(
            user=self.user,
            company_name="Acuite",
            date_of_birth=today,
            joined_on=today - timedelta(days=365 * 5),
            is_visible=True,
        )
        DirectoryProfile.objects.create(
            user=self.peer,
            company_name="Acuite",
            date_of_birth=today + timedelta(days=1),
            joined_on=today - timedelta(days=365 * 3),
            is_visible=True,
        )
        self.post = Post.objects.create(
            author=self.user,
            title="Priya's recognition",
            body="Celebrating collaboration.",
            module=Post.Module.RECOGNITION,
            topic="kudos",
            moderation_status=Post.ModerationStatus.PUBLISHED,
            published_at=timezone.now(),
        )
        Comment.objects.create(
            post=self.post,
            author=self.user,
            body="Thank you team!",
            moderation_status=Comment.ModerationStatus.PUBLISHED,
        )
        PostReaction.objects.create(post=self.post, user=self.peer)

    def test_overview_returns_points_and_celebrations(self):
        self.client.force_login(self.user)

        response = self.client.get("/api/recognition/overview/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["totals"]["kudos_posts"], 1)
        self.assertEqual(len(payload["birthdays"]), 2)
        self.assertEqual(len(payload["anniversaries"]), 2)
        self.assertGreater(payload["current_user_points"], 0)
        self.assertEqual(payload["leaderboard"][0]["name"], self.user.full_name)
