import json

from django.db.models import Count, Q
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from operations.services import record_analytics_event, record_audit_event

from .models import Comment, Post, PostReaction
from .serializers import serialize_comment, serialize_post


def _parse_json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Request body must be valid JSON.") from exc


def _can_moderate(user):
    return user.is_authenticated and (
        getattr(user, "can_moderate_connect", False)
        or user.is_staff
        or user.has_perm("feed.moderate_post")
        or user.has_perm("feed.moderate_comment")
    )


def _can_publish(user):
    return user.is_authenticated and (
        getattr(user, "can_administer_connect", False)
        or user.is_staff
        or user.has_perm("feed.publish_post")
    )


def _can_post_as_company(user):
    return user.is_authenticated and (
        getattr(user, "can_post_as_company", False)
        or user.has_perm("accounts.post_as_company")
    )


def _can_comment(user):
    return user.is_authenticated and getattr(user, "can_comment_in_connect", False)


def _can_react(user):
    return user.is_authenticated and getattr(user, "can_react_in_connect", False)


def posts_collection(request):
    if request.method == "GET":
        queryset = Post.objects.select_related("author").annotate(
            published_comment_count=Count(
                "comments",
                filter=Q(comments__moderation_status=Comment.ModerationStatus.PUBLISHED),
            ),
            like_reaction_count=Count(
                "reactions",
                filter=Q(reactions__reaction_type=PostReaction.ReactionType.LIKE),
                distinct=True,
            ),
        )
        queryset = queryset.exclude(moderation_status=Post.ModerationStatus.REMOVED)
        author_id = request.GET.get("author_id")
        if not _can_moderate(request.user):
            visible_filter = Q(moderation_status=Post.ModerationStatus.PUBLISHED)
            if (
                request.user.is_authenticated
                and author_id
                and str(request.user.pk) == str(author_id)
            ):
                visible_filter |= Q(author_id=request.user.pk)
            queryset = queryset.filter(visible_filter)

        kind = request.GET.get("kind")
        if kind:
            queryset = queryset.filter(kind=kind)

        module = request.GET.get("module")
        if module:
            queryset = queryset.filter(module=module)

        topic = request.GET.get("topic")
        if topic:
            queryset = queryset.filter(topic=topic)

        if author_id:
            queryset = queryset.filter(author_id=author_id)

        posts = [serialize_post(post, viewer=request.user) for post in queryset[:50]]
        return JsonResponse({"count": len(posts), "results": posts})

    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)
    if not getattr(request.user, "has_employee_access", False):
        return JsonResponse(
            {"detail": "This account does not currently have employee access to Acuité Connect."},
            status=403,
        )
    if not getattr(request.user, "can_create_connect_posts", False):
        return JsonResponse(
            {"detail": "Your posting access is disabled. Ask an admin to restore it."},
            status=403,
        )

    try:
        payload = _parse_json_body(request)
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    title = str(payload.get("title", "")).strip()
    body = str(payload.get("body", "")).strip()
    if not title or not body:
        return JsonResponse({"detail": "Both title and body are required."}, status=400)

    kind = payload.get("kind") or Post.PostType.UPDATE
    module = payload.get("module") or Post.Module.GENERAL
    if module not in Post.Module.values:
        return JsonResponse({"detail": "Invalid module supplied."}, status=400)

    topic = str(payload.get("topic", "")).strip().lower().replace(" ", "_")
    if len(topic) > 64:
        return JsonResponse({"detail": "Topic must be 64 characters or fewer."}, status=400)

    metadata = payload.get("metadata") or {}
    if not isinstance(metadata, dict):
        return JsonResponse({"detail": "Metadata must be a JSON object."}, status=400)

    post_as_company = bool(payload.get("post_as_company"))
    if post_as_company and not _can_post_as_company(request.user):
        return JsonResponse(
            {"detail": "Only admins can post on behalf of the company."},
            status=403,
        )
    if post_as_company:
        metadata = {
            **metadata,
            "post_as_company": True,
            "company_author_name": str(
                payload.get("company_author_name") or "Acuité Ratings & Research"
            ).strip()
            or "Acuité Ratings & Research",
            "company_author_title": str(
                payload.get("company_author_title") or "Official company post"
            ).strip()
            or "Official company post",
            "company_author_initials": str(
                payload.get("company_author_initials") or "AR"
            ).strip()[:4]
            or "AR",
        }

    visibility = payload.get("visibility") or Post.Visibility.COMPANY
    can_publish = _can_publish(request.user)
    if module == Post.Module.IDEAS_VOICE and topic == "ceo_corner" and not can_publish:
        return JsonResponse({"detail": "Only staff can publish to the CEO corner."}, status=403)

    auto_publish = can_publish or (
        module in {Post.Module.COMMUNITY, Post.Module.IDEAS_VOICE, Post.Module.RECOGNITION}
        and topic != "ceo_corner"
    )
    post = Post.objects.create(
        author=request.user,
        title=title,
        body=body,
        kind=kind,
        module=module,
        topic=topic,
        metadata=metadata,
        visibility=visibility,
        allow_comments=bool(payload.get("allow_comments", True)),
        pinned=bool(payload.get("pinned", False)) and can_publish,
        moderation_status=(
            Post.ModerationStatus.PUBLISHED
            if auto_publish
            else Post.ModerationStatus.PENDING_REVIEW
        ),
        published_at=timezone.now() if auto_publish else None,
    )
    record_audit_event(
        action="post.created",
        actor=request.user,
        target=post,
        summary=f"Created post '{post.title}'",
        metadata={
            "kind": post.kind,
            "module": post.module,
            "topic": post.topic,
            "visibility": post.visibility,
        },
        request=request,
    )
    record_analytics_event(
        "feed",
        "post_created",
        actor=request.user,
        metadata={
            "post_id": post.id,
            "module": post.module,
            "topic": post.topic,
            "moderation_status": post.moderation_status,
        },
        request=request,
    )
    return JsonResponse({"post": serialize_post(post, viewer=request.user)}, status=201)


def post_comments(request, post_id):
    post = get_object_or_404(Post.objects.select_related("author"), pk=post_id)
    if (
        post.moderation_status != Post.ModerationStatus.PUBLISHED
        and not _can_moderate(request.user)
    ):
        return JsonResponse({"detail": "Post not available."}, status=404)

    if request.method == "GET":
        queryset = post.comments.select_related("author")
        if not _can_moderate(request.user):
            queryset = queryset.filter(moderation_status=Comment.ModerationStatus.PUBLISHED)
        comments = [serialize_comment(comment) for comment in queryset]
        return JsonResponse({"count": len(comments), "results": comments})

    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    if not _can_comment(request.user):
        return JsonResponse({"detail": "Commenting is not available for this account."}, status=403)
    if not post.allow_comments:
        return JsonResponse({"detail": "Comments are disabled for this post."}, status=400)

    try:
        payload = _parse_json_body(request)
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    body = str(payload.get("body", "")).strip()
    if not body:
        return JsonResponse({"detail": "Comment body is required."}, status=400)

    comment = Comment.objects.create(
        post=post,
        author=request.user,
        body=body,
        moderation_status=Comment.ModerationStatus.PUBLISHED,
    )
    record_audit_event(
        action="comment.created",
        actor=request.user,
        target=comment,
        summary=f"Commented on '{post.title}'",
        metadata={"post_id": post.id},
        request=request,
    )
    record_analytics_event(
        "feed",
        "comment_created",
        actor=request.user,
        metadata={"comment_id": comment.id, "post_id": post.id},
        request=request,
    )
    return JsonResponse({"comment": serialize_comment(comment)}, status=201)


def toggle_post_reaction(request, post_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not _can_react(request.user):
        return JsonResponse({"detail": "Likes are not available for this account."}, status=403)

    post = get_object_or_404(Post.objects.select_related("author"), pk=post_id)
    if (
        post.moderation_status != Post.ModerationStatus.PUBLISHED
        and not _can_moderate(request.user)
    ):
        return JsonResponse({"detail": "Post not available."}, status=404)

    reaction, created = PostReaction.objects.get_or_create(
        post=post,
        user=request.user,
        reaction_type=PostReaction.ReactionType.LIKE,
    )
    reacted = created
    if not created:
        reaction.delete()
        reacted = False

    action_name = "post.liked" if reacted else "post.unliked"
    record_audit_event(
        action=action_name,
        actor=request.user,
        target=post,
        summary=f"{'Liked' if reacted else 'Removed like from'} '{post.title}'",
        metadata={"post_id": post.id, "reaction_type": PostReaction.ReactionType.LIKE},
        request=request,
    )
    record_analytics_event(
        "feed",
        "post_reaction_toggled",
        actor=request.user,
        metadata={"post_id": post.id, "reacted": reacted},
        request=request,
    )

    refreshed_post = (
        Post.objects.select_related("author")
        .annotate(
            published_comment_count=Count(
                "comments",
                filter=Q(comments__moderation_status=Comment.ModerationStatus.PUBLISHED),
            ),
            like_reaction_count=Count(
                "reactions",
                filter=Q(reactions__reaction_type=PostReaction.ReactionType.LIKE),
                distinct=True,
            ),
        )
        .get(pk=post.pk)
    )
    return JsonResponse(
        {"post": serialize_post(refreshed_post, viewer=request.user), "reacted": reacted}
    )


def post_detail(request, post_id):
    if request.method == "PATCH":
        if not request.user.is_authenticated:
            return JsonResponse({"detail": "Authentication required."}, status=403)
        if not _can_publish(request.user):
            return JsonResponse({"detail": "Admin access is required to review posts."}, status=403)

        try:
            payload = _parse_json_body(request)
        except ValueError as exc:
            return JsonResponse({"detail": str(exc)}, status=400)

        post = get_object_or_404(Post.objects.select_related("author"), pk=post_id)
        status = str(payload.get("moderation_status", "")).strip().lower()
        if status not in {
            Post.ModerationStatus.PUBLISHED,
            Post.ModerationStatus.REJECTED,
        }:
            return JsonResponse({"detail": "Unsupported moderation status."}, status=400)

        post.moderation_status = status
        update_fields = ["moderation_status", "updated_at"]
        if status == Post.ModerationStatus.PUBLISHED:
            post.published_at = post.published_at or timezone.now()
            update_fields.append("published_at")
        post.save(update_fields=update_fields)

        action_name = "post.published" if status == Post.ModerationStatus.PUBLISHED else "post.rejected"
        record_audit_event(
            action=action_name,
            actor=request.user,
            target=post,
            summary=f"{'Published' if status == Post.ModerationStatus.PUBLISHED else 'Rejected'} post '{post.title}'",
            metadata={"post_id": post.id, "moderation_status": status},
            request=request,
        )
        record_analytics_event(
            "moderation",
            "post_reviewed",
            actor=request.user,
            metadata={"post_id": post.id, "moderation_status": status},
            request=request,
        )
        refreshed_post = (
            Post.objects.select_related("author")
            .annotate(
                published_comment_count=Count(
                    "comments",
                    filter=Q(comments__moderation_status=Comment.ModerationStatus.PUBLISHED),
                ),
                like_reaction_count=Count(
                    "reactions",
                    filter=Q(reactions__reaction_type=PostReaction.ReactionType.LIKE),
                    distinct=True,
                ),
            )
            .get(pk=post.pk)
        )
        return JsonResponse({"post": serialize_post(refreshed_post, viewer=request.user)})

    if request.method != "DELETE":
        return HttpResponseNotAllowed(["PATCH", "DELETE"])
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)

    post = get_object_or_404(Post.objects.select_related("author"), pk=post_id)
    if post.moderation_status == Post.ModerationStatus.REMOVED:
        return JsonResponse({"detail": "Post not available."}, status=404)

    is_author = request.user.pk == post.author_id
    is_moderator = _can_moderate(request.user)
    if not is_author and not is_moderator:
        return JsonResponse({"detail": "You do not have permission to delete this post."}, status=403)

    post.moderation_status = Post.ModerationStatus.REMOVED
    post.pinned = False
    post.save(update_fields=["moderation_status", "pinned", "updated_at"])

    action_name = "post.deleted_by_author" if is_author and not is_moderator else "post.removed_by_moderator"
    summary = (
        f"Deleted own post '{post.title}'"
        if is_author and not is_moderator
        else f"Removed post '{post.title}'"
    )
    record_audit_event(
        action=action_name,
        actor=request.user,
        target=post,
        summary=summary,
        metadata={"post_id": post.id, "post_author_id": post.author_id},
        request=request,
    )
    record_analytics_event(
        "feed",
        "post_deleted",
        actor=request.user,
        metadata={
            "post_id": post.id,
            "deleted_by_author": is_author,
            "deleted_by_moderator": is_moderator and not is_author,
            "module": post.module,
            "topic": post.topic,
        },
        request=request,
    )
    return JsonResponse({"detail": "Post deleted successfully.", "post_id": post.id})
