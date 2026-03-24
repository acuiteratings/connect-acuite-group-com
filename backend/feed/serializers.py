from accounts.serializers import serialize_user

from .models import Comment, PostReaction


def serialize_post(post, *, viewer=None):
    metadata = post.metadata or {}
    author = serialize_user(post.author)
    if metadata.get("post_as_company"):
        author = {
            **author,
            "name": metadata.get("company_author_name", "Acuité Ratings & Research"),
            "title": metadata.get("company_author_title", "Official company post"),
            "initials": metadata.get("company_author_initials", "AR"),
            "is_company": True,
        }
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
    viewer_is_author = False
    viewer_can_delete = False
    if viewer and getattr(viewer, "is_authenticated", False):
        viewer_is_author = post.author_id == viewer.id
        current_user_has_reacted = post.reactions.filter(
            user=viewer,
            reaction_type=PostReaction.ReactionType.LIKE,
        ).exists()
        viewer_can_delete = viewer_is_author or bool(
            getattr(viewer, "can_moderate_connect", False)
            or getattr(viewer, "is_staff", False)
            or viewer.has_perm("feed.moderate_post")
            or viewer.has_perm("feed.moderate_comment")
        )
    return {
        "id": post.id,
        "title": post.title,
        "body": post.body,
        "kind": post.kind,
        "module": post.module,
        "topic": post.topic,
        "metadata": metadata,
        "posted_as_company": bool(metadata.get("post_as_company")),
        "visibility": post.visibility,
        "moderation_status": post.moderation_status,
        "allow_comments": post.allow_comments,
        "pinned": post.pinned,
        "published_at": post.published_at.isoformat() if post.published_at else None,
        "created_at": post.created_at.isoformat(),
        "updated_at": post.updated_at.isoformat(),
        "author_user_id": post.author_id,
        "author": author,
        "comment_count": comment_count,
        "reaction_count": reaction_count,
        "current_user_has_reacted": current_user_has_reacted,
        "viewer_is_author": viewer_is_author,
        "viewer_can_delete": viewer_can_delete,
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
