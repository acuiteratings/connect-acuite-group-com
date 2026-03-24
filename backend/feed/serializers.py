from accounts.serializers import serialize_user

from .models import Comment, PostReaction


def serialize_post(post, *, viewer=None):
    comment_count = getattr(
        post,
        "published_comment_count",
        post.comments.filter(
            moderation_status=Comment.ModerationStatus.PUBLISHED
        ).count(),
    )
    reaction_count = getattr(
        post,
        "like_reaction_count",
        post.reactions.filter(reaction_type=PostReaction.ReactionType.LIKE).count(),
    )
    current_user_has_reacted = False
    if viewer and getattr(viewer, "is_authenticated", False):
        current_user_has_reacted = post.reactions.filter(
            user=viewer,
            reaction_type=PostReaction.ReactionType.LIKE,
        ).exists()
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
        "reaction_count": reaction_count,
        "current_user_has_reacted": current_user_has_reacted,
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
