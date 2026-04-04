import json
from datetime import datetime, timedelta
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from accounts.models import ExitProcess, User
from directory.models import DirectoryProfile
from feed.models import Comment, Post, PostReaction

from .models import BrandStoreItem, BrandStoreRedemption, CoinLedgerEntry
from .services import backfill_coin_ledger


class BrandStoreApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="reshma.polasa@acuite.in",
            password="testpass123",
            first_name="Reshma",
            last_name="Polasa",
            title="Head - Operations",
        )
        self.admin = User.objects.create_user(
            email="admin@acuite.in",
            password="testpass123",
            first_name="Admin",
            last_name="User",
            access_level=User.AccessLevel.ADMIN,
            is_staff=True,
        )
        DirectoryProfile.objects.create(
            user=self.user,
            company_name="Acuite",
            department_for_connect="Corporate",
            date_of_birth=timezone.localdate() + timedelta(days=7),
            joined_on=timezone.localdate() - timedelta(days=365 * 4),
            is_visible=True,
        )
        DirectoryProfile.objects.create(
            user=self.admin,
            company_name="Acuite",
            department_for_connect="Corporate",
            is_visible=True,
        )
        self.post = Post.objects.create(
            author=self.user,
            title="Recognition post",
            body="Great teamwork on rollout.",
            module=Post.Module.BULLETIN,
            topic="announcements",
            moderation_status=Post.ModerationStatus.PUBLISHED,
            published_at=timezone.now(),
        )
        PostReaction.objects.create(post=self.post, user=self.user)
        Comment.objects.create(post=self.post, author=self.user, body="Great update.")
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
        self.assertTrue(any(item["name"] == "Acuite Mug" for item in payload["items"]))
        self.assertGreaterEqual(payload["balance"]["earned_points"], 10)
        self.assertIn("spent_points", payload["balance"])
        self.assertIn("register", payload["balance"])
        self.assertTrue(any(item["name"] == "Acuite Coffee Mug" for item in payload["items"]))
        self.assertEqual(payload["balance"]["locked_points"], 0)

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

    def test_pending_redemption_counts_against_new_request_eligibility(self):
        second_item = BrandStoreItem.objects.create(
            name="Acuite Pen",
            category=BrandStoreItem.Category.DESK,
            description="Premium pen",
            point_cost=10,
            stock_units=5,
            is_active=True,
        )
        self.client.force_login(self.user)

        first_response = self.client.post(
            "/api/store/redemptions/",
            data=json.dumps({"item_id": self.item.id}),
            content_type="application/json",
        )
        second_response = self.client.post(
            "/api/store/redemptions/",
            data=json.dumps({"item_id": second_item.id}),
            content_type="application/json",
        )

        self.assertEqual(first_response.status_code, 201)
        self.assertEqual(second_response.status_code, 400)
        self.assertEqual(
            second_response.json()["detail"],
            "Not enough Acuite Coins available for this request.",
        )

    def test_requester_can_cancel_requested_redemption(self):
        redemption = BrandStoreRedemption.objects.create(
            item=self.item,
            requester=self.user,
            points_locked=self.item.point_cost,
        )
        self.client.force_login(self.user)

        response = self.client.patch(
            f"/api/store/redemptions/{redemption.id}/",
            data=json.dumps({"status": "cancelled"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        redemption.refresh_from_db()
        self.assertEqual(redemption.status, BrandStoreRedemption.Status.CANCELLED)

    def test_admin_can_approve_store_redemption(self):
        redemption = BrandStoreRedemption.objects.create(
            item=self.item,
            requester=self.user,
            points_locked=self.item.point_cost,
        )
        self.client.force_login(self.admin)

        response = self.client.patch(
            f"/api/store/redemptions/{redemption.id}/",
            data=json.dumps({"status": "approved"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        redemption.refresh_from_db()
        self.assertEqual(redemption.status, BrandStoreRedemption.Status.APPROVED)
        self.assertIsNotNone(redemption.reviewed_at)

    def test_admin_overview_returns_requested_redemptions(self):
        BrandStoreRedemption.objects.create(
            item=self.item,
            requester=self.user,
            points_locked=self.item.point_cost,
        )
        self.client.force_login(self.admin)

        response = self.client.get("/api/store/admin/overview/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(len(payload["requests"]), 1)

    def test_town_hall_reward_is_added_only_after_admin_approval(self):
        Post.objects.create(
            author=self.user,
            title="Town hall response",
            body="I have a question.",
            module=Post.Module.EMPLOYEE_POSTS,
            topic="employee_submission",
            moderation_status=Post.ModerationStatus.PENDING_REVIEW,
            metadata={
                "town_hall_response": True,
                "submission_key": "town_hall_response",
            },
        )
        self.client.force_login(self.user)

        pending_response = self.client.get("/api/store/overview/")
        self.assertEqual(pending_response.status_code, 200)
        pending_earned = pending_response.json()["balance"]["earned_points"]

        post = Post.objects.get(title="Town hall response")
        post.moderation_status = Post.ModerationStatus.PUBLISHED
        post.published_at = timezone.now()
        post.save(update_fields=["moderation_status", "published_at", "updated_at"])

        approved_response = self.client.get("/api/store/overview/")
        self.assertEqual(approved_response.status_code, 200)
        self.assertEqual(approved_response.json()["balance"]["earned_points"], pending_earned + 1000)

    def test_share_idea_reward_is_added_only_after_admin_approval(self):
        Post.objects.create(
            author=self.user,
            title="Idea to improve workflow",
            body="Share review checklist improvements.",
            module=Post.Module.EMPLOYEE_POSTS,
            topic="employee_submission",
            moderation_status=Post.ModerationStatus.PENDING_REVIEW,
            metadata={
                "submission_key": "share_idea",
            },
        )
        self.client.force_login(self.user)

        pending_response = self.client.get("/api/store/overview/")
        pending_earned = pending_response.json()["balance"]["earned_points"]

        post = Post.objects.get(title="Idea to improve workflow")
        post.moderation_status = Post.ModerationStatus.PUBLISHED
        post.published_at = timezone.now()
        post.save(update_fields=["moderation_status", "published_at", "updated_at"])

        approved_response = self.client.get("/api/store/overview/")
        self.assertEqual(approved_response.json()["balance"]["earned_points"], pending_earned + 500)

    def test_ceo_request_reward_is_added_only_after_admin_approval(self):
        Post.objects.create(
            author=self.user,
            title="Ready for a cup of masala chai with me?",
            body="Employee selected: Ready for a cup of masala chai with me?",
            module=Post.Module.EMPLOYEE_POSTS,
            topic="employee_submission",
            moderation_status=Post.ModerationStatus.PENDING_REVIEW,
            metadata={
                "ceo_desk_request": True,
                "ceo_desk_request_key": "masala_chai",
            },
        )
        self.client.force_login(self.user)

        pending_response = self.client.get("/api/store/overview/")
        pending_earned = pending_response.json()["balance"]["earned_points"]

        post = Post.objects.get(title="Ready for a cup of masala chai with me?")
        post.moderation_status = Post.ModerationStatus.PUBLISHED
        post.published_at = timezone.now()
        post.save(update_fields=["moderation_status", "published_at", "updated_at"])

        approved_response = self.client.get("/api/store/overview/")
        self.assertEqual(approved_response.json()["balance"]["earned_points"], pending_earned + 1000)

    def test_requested_store_item_does_not_reduce_balance_until_admin_approval(self):
        self.client.force_login(self.user)

        before_response = self.client.get("/api/store/overview/")
        before_balance = before_response.json()["balance"]

        create_response = self.client.post(
            "/api/store/redemptions/",
            data=json.dumps({"item_id": self.item.id}),
            content_type="application/json",
        )
        self.assertEqual(create_response.status_code, 201)

        requested_response = self.client.get("/api/store/overview/")
        requested_balance = requested_response.json()["balance"]
        self.assertEqual(requested_balance["locked_points"], self.item.point_cost)
        self.assertEqual(requested_balance["spent_points"], before_balance["spent_points"])
        self.assertEqual(
            requested_balance["available_points"],
            before_balance["available_points"] - self.item.point_cost,
        )

        redemption = BrandStoreRedemption.objects.get()
        self.client.force_login(self.admin)
        approve_response = self.client.patch(
            f"/api/store/redemptions/{redemption.id}/",
            data=json.dumps({"status": "approved"}),
            content_type="application/json",
        )
        self.assertEqual(approve_response.status_code, 200)

        self.client.force_login(self.user)
        approved_balance = self.client.get("/api/store/overview/").json()["balance"]
        self.assertEqual(approved_balance["spent_points"], before_balance["spent_points"] + self.item.point_cost)

    def test_like_reversal_creates_offset_ledger_entries(self):
        extra_post = Post.objects.create(
            author=self.user,
            title="Second post",
            body="Another update.",
            module=Post.Module.BULLETIN,
            topic="announcements",
            moderation_status=Post.ModerationStatus.PUBLISHED,
            published_at=timezone.now(),
        )
        self.client.force_login(self.admin)
        reaction = PostReaction.objects.create(post=extra_post, user=self.admin)

        earned_after_like = self.client.get("/api/store/overview/").json()["balance"]["earned_points"]
        reaction.delete()
        earned_after_unlike = self.client.get("/api/store/overview/").json()["balance"]["earned_points"]

        self.assertEqual(
            CoinLedgerEntry.objects.filter(
                user=self.admin,
                event_key="reaction_given",
                entry_type=CoinLedgerEntry.EntryType.EARN,
            ).count(),
            1,
        )
        self.assertEqual(
            CoinLedgerEntry.objects.filter(
                user=self.admin,
                event_key="reaction_given",
                entry_type=CoinLedgerEntry.EntryType.EARN_REVERSAL,
            ).count(),
            1,
        )
        self.assertEqual(earned_after_like - earned_after_unlike, 1)

    def test_redemption_creates_hold_then_release_and_spend_entries(self):
        redemption = BrandStoreRedemption.objects.create(
            item=self.item,
            requester=self.user,
            points_locked=self.item.point_cost,
        )

        self.assertEqual(
            CoinLedgerEntry.objects.filter(
                reference_key=f"redemption:{redemption.id}:store_request:hold"
            ).count(),
            1,
        )
        self.assertEqual(
            CoinLedgerEntry.objects.filter(
                reference_key=f"redemption:{redemption.id}:store_request:release"
            ).count(),
            0,
        )
        self.assertEqual(
            CoinLedgerEntry.objects.filter(
                reference_key=f"redemption:{redemption.id}:store_request:spend"
            ).count(),
            0,
        )

        redemption.status = BrandStoreRedemption.Status.APPROVED
        redemption.reviewed_at = timezone.now()
        redemption.save(update_fields=["status", "reviewed_at", "updated_at"])

        self.assertEqual(
            CoinLedgerEntry.objects.filter(
                reference_key=f"redemption:{redemption.id}:store_request:release"
            ).count(),
            1,
        )
        self.assertEqual(
            CoinLedgerEntry.objects.filter(
                reference_key=f"redemption:{redemption.id}:store_request:spend"
            ).count(),
            1,
        )

    def test_backfill_coin_ledger_rebuilds_entries_without_duplication(self):
        CoinLedgerEntry.objects.all().delete()

        backfill_coin_ledger()

        self.assertTrue(
            CoinLedgerEntry.objects.filter(
                user=self.user,
                event_key="reaction_given",
                entry_type=CoinLedgerEntry.EntryType.EARN,
            ).exists()
        )
        self.assertTrue(
            CoinLedgerEntry.objects.filter(
                user=self.user,
                event_key="published_comment",
                entry_type=CoinLedgerEntry.EntryType.EARN,
            ).exists()
        )
        first_count = CoinLedgerEntry.objects.count()
        backfill_coin_ledger()
        self.assertEqual(CoinLedgerEntry.objects.count(), first_count)

    def test_financial_year_end_expires_unused_available_points(self):
        CoinLedgerEntry.objects.all().delete()
        self.client.force_login(self.user)
        expiry_now = timezone.make_aware(datetime(2026, 4, 4, 9, 0, 0))
        earn_time = timezone.make_aware(datetime(2026, 3, 15, 10, 0, 0))

        CoinLedgerEntry.objects.create(
            user=self.user,
            entry_type=CoinLedgerEntry.EntryType.EARN,
            event_key="question_asked",
            amount=1000,
            reference_key="manual-test-earn-fy",
            summary="Manual fiscal-year earn",
            occurred_at=earn_time,
        )

        with patch("store.services.timezone.now", return_value=expiry_now):
            balance = self.client.get("/api/store/overview/").json()["balance"]

        self.assertEqual(balance["earned_points"], 1000)
        self.assertEqual(balance["expired_points"], 1000)
        self.assertEqual(balance["available_points"], 0)
        self.assertTrue(
            CoinLedgerEntry.objects.filter(
                user=self.user,
                entry_type=CoinLedgerEntry.EntryType.EXPIRE,
                reference_key="coin_expiry:fiscal_year_end:2026-04-01",
            ).exists()
        )

    def test_exit_day_expires_unused_available_points(self):
        CoinLedgerEntry.objects.all().delete()
        self.client.force_login(self.user)
        earn_time = timezone.make_aware(datetime(2026, 4, 10, 10, 0, 0))
        exit_now = timezone.make_aware(datetime(2026, 4, 18, 10, 0, 0))

        CoinLedgerEntry.objects.create(
            user=self.user,
            entry_type=CoinLedgerEntry.EntryType.EARN,
            event_key="idea_shared",
            amount=500,
            reference_key="manual-test-earn-exit",
            summary="Manual exit earn",
            occurred_at=earn_time,
        )
        ExitProcess.objects.create(
            employee=self.user,
            initiated_by=self.admin,
            updated_by=self.admin,
            resignation_date=datetime(2026, 4, 15).date(),
            last_working_day=datetime(2026, 4, 18).date(),
            stage=ExitProcess.Stage.ALUMNI_CONVERSION,
            notes="Exit scheduled.",
        )

        with patch("store.services.timezone.now", return_value=exit_now):
            balance = self.client.get("/api/store/overview/").json()["balance"]

        self.assertEqual(balance["earned_points"], 500)
        self.assertEqual(balance["expired_points"], 500)
        self.assertEqual(balance["available_points"], 0)
        self.assertTrue(
            CoinLedgerEntry.objects.filter(
                user=self.user,
                entry_type=CoinLedgerEntry.EntryType.EXPIRE,
                reference_key="coin_expiry:employee_exit:2026-04-18",
            ).exists()
        )
