from django.contrib import admin
from django.utils import timezone

from operations.services import record_analytics_event, record_audit_event

from .models import Comment, Post, PostReaction


@admin.action(description="Publish selected posts")
def publish_posts(_modeladmin, request, queryset):
    for post in queryset:
        post.moderation_status = Post.ModerationStatus.PUBLISHED
        post.published_at = post.published_at or timezone.now()
        post.save(update_fields=["moderation_status", "published_at", "updated_at"])
        record_audit_event(
            action="post.published",
            actor=request.user,
            target=post,
            summary=f"Published post '{post.title}'",
            request=request,
        )
        record_analytics_event(
            "moderation",
            "post_published_admin",
            actor=request.user,
            metadata={"post_id": post.id},
            request=request,
        )


@admin.action(description="Reject selected posts")
def reject_posts(_modeladmin, request, queryset):
    for post in queryset:
        post.moderation_status = Post.ModerationStatus.REJECTED
        post.save(update_fields=["moderation_status", "updated_at"])
        record_audit_event(
            action="post.rejected",
            actor=request.user,
            target=post,
            summary=f"Rejected post '{post.title}'",
            request=request,
        )
        record_analytics_event(
            "moderation",
            "post_rejected_admin",
            actor=request.user,
            metadata={"post_id": post.id},
            request=request,
        )


@admin.action(description="Publish selected comments")
def publish_comments(_modeladmin, request, queryset):
    for comment in queryset:
        comment.moderation_status = Comment.ModerationStatus.PUBLISHED
        comment.save(update_fields=["moderation_status", "updated_at"])
        record_audit_event(
            action="comment.published",
            actor=request.user,
            target=comment,
            summary=f"Published comment on '{comment.post.title}'",
            request=request,
        )
        record_analytics_event(
            "moderation",
            "comment_published_admin",
            actor=request.user,
            metadata={"comment_id": comment.id, "post_id": comment.post_id},
            request=request,
        )


@admin.action(description="Remove selected comments")
def remove_comments(_modeladmin, request, queryset):
    for comment in queryset:
        comment.moderation_status = Comment.ModerationStatus.REMOVED
        comment.save(update_fields=["moderation_status", "updated_at"])
        record_audit_event(
            action="comment.removed",
            actor=request.user,
            target=comment,
            summary=f"Removed comment on '{comment.post.title}'",
            request=request,
        )
        record_analytics_event(
            "moderation",
            "comment_removed_admin",
            actor=request.user,
            metadata={"comment_id": comment.id, "post_id": comment.post_id},
            request=request,
        )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "module",
        "topic",
        "kind",
        "visibility",
        "moderation_status",
        "pinned",
        "published_at",
        "created_at",
    )
    list_filter = ("module", "kind", "visibility", "moderation_status", "pinned")
    search_fields = (
        "title",
        "body",
        "topic",
        "author__email",
        "author__first_name",
        "author__last_name",
    )
    autocomplete_fields = ("author",)
    actions = (publish_posts, reject_posts)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "moderation_status", "created_at")
    list_filter = ("moderation_status", "created_at")
    search_fields = ("body", "author__email", "post__title")
    autocomplete_fields = ("post", "author")
    actions = (publish_comments, remove_comments)


@admin.register(PostReaction)
class PostReactionAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "reaction_type", "updated_at")
    list_filter = ("reaction_type", "updated_at")
    search_fields = ("post__title", "user__email", "user__first_name", "user__last_name")
    autocomplete_fields = ("post", "user")
