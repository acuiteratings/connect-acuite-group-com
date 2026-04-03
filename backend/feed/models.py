from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    class PostType(models.TextChoices):
        ANNOUNCEMENT = "announcement", "Announcement"
        UPDATE = "update", "Update"
        KUDOS = "kudos", "Kudos"
        POLL = "poll", "Poll"
        RESOURCE = "resource", "Resource"

    class Module(models.TextChoices):
        BULLETIN = "bulletin", "Bulletin Board"
        EMPLOYEE_POSTS = "employee_posts", "Employee Posts"

    class Visibility(models.TextChoices):
        COMPANY = "company", "Company-wide"
        DEPARTMENT = "department", "Department"
        LEADERSHIP = "leadership", "Leadership"

    class ModerationStatus(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING_REVIEW = "pending_review", "Pending review"
        PUBLISHED = "published", "Published"
        REJECTED = "rejected", "Rejected"
        REMOVED = "removed", "Removed"

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    title = models.CharField(max_length=180)
    body = models.TextField()
    kind = models.CharField(max_length=24, choices=PostType.choices, default=PostType.UPDATE)
    module = models.CharField(
        max_length=32,
        choices=Module.choices,
        default=Module.BULLETIN,
    )
    topic = models.CharField(max_length=64, blank=True, default="")
    metadata = models.JSONField(default=dict, blank=True)
    visibility = models.CharField(
        max_length=24,
        choices=Visibility.choices,
        default=Visibility.COMPANY,
    )
    moderation_status = models.CharField(
        max_length=24,
        choices=ModerationStatus.choices,
        default=ModerationStatus.DRAFT,
    )
    allow_comments = models.BooleanField(default=True)
    pinned = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-pinned", "-published_at", "-created_at")
        permissions = [
            ("moderate_post", "Can moderate posts"),
            ("publish_post", "Can publish posts"),
        ]

    def __str__(self):
        return self.title

    def publish(self):
        self.moderation_status = self.ModerationStatus.PUBLISHED
        self.published_at = self.published_at or timezone.now()
        self.save(update_fields=["moderation_status", "published_at", "updated_at"])


class Comment(models.Model):
    class ModerationStatus(models.TextChoices):
        PUBLISHED = "published", "Published"
        PENDING_REVIEW = "pending_review", "Pending review"
        REJECTED = "rejected", "Rejected"
        REMOVED = "removed", "Removed"

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
    )
    body = models.TextField()
    moderation_status = models.CharField(
        max_length=24,
        choices=ModerationStatus.choices,
        default=ModerationStatus.PUBLISHED,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("created_at",)
        permissions = [
            ("moderate_comment", "Can moderate comments"),
        ]

    def __str__(self):
        return f"Comment by {self.author.full_name} on {self.post.title}"


class PostReaction(models.Model):
    class ReactionType(models.TextChoices):
        LIKE = "like", "Like"

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="reactions")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="post_reactions",
    )
    reaction_type = models.CharField(
        max_length=16,
        choices=ReactionType.choices,
        default=ReactionType.LIKE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-updated_at",)
        constraints = [
            models.UniqueConstraint(
                fields=("post", "user", "reaction_type"),
                name="feed_unique_reaction_per_post_user_type",
            )
        ]

    def __str__(self):
        return f"{self.user.full_name} reacted to {self.post.title}"
