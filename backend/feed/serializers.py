from accounts.serializers import serialize_user

from .models import Comment


def serialize_post(post):
    comment_count = getattr(
        post,
        "published_comment_count",
        post.comments.filter(
            moderation_status=Comment.ModerationStatus.PUBLISHED
        ).count(),
    )
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "kind": post.kind,
        "module": post.module,
        "topic": post.topic,
        "metadata": post.metadata or {},
        "visibility": post.visibility,
        "moderation_status": post.moderation_status,
        "allow_comments": post.allow_comments,
        "pinned": post.pinned,
        "published_at": post.published_at.isoformat() if post.published_at else None,
        "created_at": post.created_at.isoformat(),
        "updated_at": post.updated_at.isoformat(),
        "author": serialize_user(post.author),
        "comment_count": comment_count,
    }


def serialize_comment(comment):
    return {
        "id": comment.id,
        "body": comment.body,
        "moderation_status": comment.moderation_status,
        "created_at": comment.created_at.isoformat(),
        "updated_at": comment.updated_at.isoformat(),
        "author": serialize_user(comment.author),
        "post_id": comment.post_id,
    }
