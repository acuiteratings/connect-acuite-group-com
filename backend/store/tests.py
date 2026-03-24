import json
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from directory.models import DirectoryProfile
from feed.models import Post, PostReaction

from .models import BrandStoreItem, BrandStoreRedemption


class BrandStoreApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="reshma.polasa@acuite.in",
            password="testpass123",
            first_name="Reshma",
            last_name="Polasa",
            title="Head - Operations",
        )
        DirectoryProfile.objects.create(
            user=self.user,
            company_name="Acuite",
            department_for_connect="Corporate",
            date_of_birth=timezone.localdate() + timedelta(days=7),
            joined_on=timezone.localdate() - timedelta(days=365 * 4),
            is_visible=True,
        )
        self.post = Post.objects.create(
            author=self.user,
            title="Recognition post",
            body="Great teamwork on rollout.",
            module=Post.Module.RECOGNITION,
            topic="kudos",
            moderation_status=Post.ModerationStatus.PUBLISHED,
            published_at=timezone.now(),
        )
        PostReaction.objects.create(post=self.post, user=self.user)
        self.item = BrandStoreItem.objects.create(
            name="Acuite Mug",
            category=BrandStoreItem.Category.DRINKWARE,
            description="Ceramic mug",
            point_cost=10,
            stock_units=5,
            is_active=True,
        )

    def test_store_overview_returns_balance_and_items(self):
        self.client.force_login(self.user)

        response = self.client.get("/api/store/overview/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload["items"]), 1)
        self.assertGreaterEqual(payload["balance"]["earned_points"], 10)

    def test_user_can_request_redemption_when_points_are_available(self):
        self.client.force_login(self.user)

        response = self.client.post(
            "/api/store/redemptions/",
            data=json.dumps({"item_id": self.item.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(BrandStoreRedemption.objects.count(), 1)
        self.assertEqual(response.json()["redemption"]["item"]["name"], "Acuite Mug")
