import json

from django.test import Client, TestCase

from accounts.models import User
from operations.models import AnalyticsEvent, AuditLog

from .models import Comment, Post, PostReaction


class FeedApiTests(TestCase):
    def setUp(self):
        self.csrf_client = Client(enforce_csrf_checks=True)
        self.user = User.objects.create_user(
            email="rahul.mehta@acuite.in",
            password="testpass123",
            first_name="Rahul",
            last_name="Mehta",
            title="Senior Analyst",
            department="Ratings",
        )
        self.admin_user = User.objects.create_user(
            email="admin.connect@acuite.in",
            password="testpass123",
            first_name="Acuite",
            last_name="Admin",
            access_level=User.AccessLevel.ADMIN,
            must_change_password=False,
        )
        self.moderator_user = User.objects.create_user(
            email="moderator.connect@acuite.in",
            password="testpass123",
            first_name="Acuite",
            last_name="Moderator",
            access_level=User.AccessLevel.MODERATOR,
            must_change_password=False,
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

    def test_post_creation_requires_csrf_token(self):
        self.csrf_client.force_login(self.user)

        response = self.csrf_client.post(
            "/api/feed/posts/",
            data=json.dumps({"title": "Hello", "body": "First backend post"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Post.objects.count(), 0)

    def test_user_with_posting_disabled_cannot_create_post(self):
        self.user.can_post_in_connect = False
        self.user.save(update_fields=["can_post_in_connect", "updated_at"])
        self.client.force_login(self.user)

        response = self.client.post(
            "/api/feed/posts/",
            data=json.dumps({"title": "Blocked", "body": "This should fail"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            response.json()["detail"],
            "Your posting access is disabled. Ask an admin to restore it.",
        )
        self.assertEqual(Post.objects.count(), 0)

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

    def test_admin_can_post_ceo_corner_as_company(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            "/api/feed/posts/",
            data=json.dumps(
                {
                    "title": "Leadership note",
                    "body": "A direct note to everyone.",
                    "module": "ideas_voice",
                    "topic": "ceo_corner",
                    "post_as_company": True,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()["post"]
        self.assertEqual(payload["moderation_status"], Post.ModerationStatus.PUBLISHED)
        self.assertTrue(payload["posted_as_company"])
        self.assertEqual(payload["author"]["name"], "Acuité Ratings & Research")

    def test_user_with_posting_disabled_can_still_comment_and_like(self):
        post = Post.objects.create(
            author=self.admin_user,
            title="Published post",
            body="Visible to the company",
            moderation_status=Post.ModerationStatus.PUBLISHED,
        )
        self.user.can_post_in_connect = False
        self.user.save(update_fields=["can_post_in_connect", "updated_at"])
        self.client.force_login(self.user)

        comment_response = self.client.post(
            f"/api/feed/posts/{post.id}/comments/",
            data=json.dumps({"body": "Still able to comment."}),
            content_type="application/json",
        )
        like_response = self.client.post(f"/api/feed/posts/{post.id}/reactions/toggle/")

        self.assertEqual(comment_response.status_code, 201)
        self.assertEqual(like_response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(PostReaction.objects.count(), 1)

    def test_authenticated_user_can_toggle_like_reaction(self):
        post = Post.objects.create(
            author=self.user,
            title="Recognition post",
            body="Visible post",
            module=Post.Module.RECOGNITION,
            topic="kudos",
            moderation_status=Post.ModerationStatus.PUBLISHED,
        )
        self.client.force_login(self.user)

        first_response = self.client.post(f"/api/feed/posts/{post.id}/reactions/toggle/")

        self.assertEqual(first_response.status_code, 200)
        self.assertTrue(first_response.json()["reacted"])
        self.assertEqual(first_response.json()["post"]["reaction_count"], 1)
        self.assertTrue(first_response.json()["post"]["current_user_has_reacted"])
        self.assertEqual(PostReaction.objects.count(), 1)

        second_response = self.client.post(f"/api/feed/posts/{post.id}/reactions/toggle/")

        self.assertEqual(second_response.status_code, 200)
        self.assertFalse(second_response.json()["reacted"])
        self.assertEqual(second_response.json()["post"]["reaction_count"], 0)
        self.assertFalse(second_response.json()["post"]["current_user_has_reacted"])
        self.assertEqual(PostReaction.objects.count(), 0)

    def test_author_can_delete_own_post(self):
        post = Post.objects.create(
            author=self.user,
            title="Own post",
            body="Delete me",
            moderation_status=Post.ModerationStatus.PUBLISHED,
        )
        self.client.force_login(self.user)

        response = self.client.delete(f"/api/feed/posts/{post.id}/")

        self.assertEqual(response.status_code, 200)
        post.refresh_from_db()
        self.assertEqual(post.moderation_status, Post.ModerationStatus.REMOVED)

    def test_admin_can_publish_pending_post(self):
        post = Post.objects.create(
            author=self.user,
            title="Pending post",
            body="Needs approval",
            moderation_status=Post.ModerationStatus.PENDING_REVIEW,
        )
        self.client.force_login(self.admin_user)

        response = self.client.patch(
            f"/api/feed/posts/{post.id}/",
            data=json.dumps({"moderation_status": "published"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        post.refresh_from_db()
        self.assertEqual(post.moderation_status, Post.ModerationStatus.PUBLISHED)
        self.assertIsNotNone(post.published_at)

    def test_admin_can_reject_pending_post(self):
        post = Post.objects.create(
            author=self.user,
            title="Pending post",
            body="Needs approval",
            moderation_status=Post.ModerationStatus.PENDING_REVIEW,
        )
        self.client.force_login(self.admin_user)

        response = self.client.patch(
            f"/api/feed/posts/{post.id}/",
            data=json.dumps({"moderation_status": "rejected"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        post.refresh_from_db()
        self.assertEqual(post.moderation_status, Post.ModerationStatus.REJECTED)

    def test_employee_can_list_own_pending_posts_with_author_filter(self):
        own_pending = Post.objects.create(
            author=self.user,
            title="My pending post",
            body="Still waiting",
            module=Post.Module.GENERAL,
            topic="employee_submission",
            moderation_status=Post.ModerationStatus.PENDING_REVIEW,
        )
        Post.objects.create(
            author=self.admin_user,
            title="Other pending post",
            body="Should stay hidden",
            module=Post.Module.GENERAL,
            topic="employee_submission",
            moderation_status=Post.ModerationStatus.PENDING_REVIEW,
        )
        self.client.force_login(self.user)

        response = self.client.get(f"/api/feed/posts/?module=general&topic=employee_submission&author_id={self.user.id}")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["results"][0]["id"], own_pending.id)
        self.assertEqual(
            payload["results"][0]["moderation_status"],
            Post.ModerationStatus.PENDING_REVIEW,
        )

    def test_moderator_can_delete_any_post(self):
        post = Post.objects.create(
            author=self.user,
            title="Moderate me",
            body="Please remove",
            moderation_status=Post.ModerationStatus.PUBLISHED,
        )
        self.client.force_login(self.moderator_user)

        response = self.client.delete(f"/api/feed/posts/{post.id}/")

        self.assertEqual(response.status_code, 200)
        post.refresh_from_db()
        self.assertEqual(post.moderation_status, Post.ModerationStatus.REMOVED)

    def test_employee_cannot_delete_someone_elses_post(self):
        post = Post.objects.create(
            author=self.admin_user,
            title="Not yours",
            body="Protected",
            moderation_status=Post.ModerationStatus.PUBLISHED,
        )
        self.client.force_login(self.user)

        response = self.client.delete(f"/api/feed/posts/{post.id}/")

        self.assertEqual(response.status_code, 403)
        post.refresh_from_db()
        self.assertEqual(post.moderation_status, Post.ModerationStatus.PUBLISHED)
