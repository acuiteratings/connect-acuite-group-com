import json

from django.db.models import Count, Q
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from operations.services import record_analytics_event, record_audit_event

from .models import Comment, Post
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
        user.is_staff
        or user.has_perm("feed.moderate_post")
        or user.has_perm("feed.moderate_comment")
    )


def _can_publish(user):
    return user.is_authenticated and (user.is_staff or user.has_perm("feed.publish_post"))


@csrf_exempt
def posts_collection(request):
    if request.method == "GET":
        queryset = Post.objects.select_related("author").annotate(
            published_comment_count=Count(
                "comments",
                filter=Q(comments__moderation_status=Comment.ModerationStatus.PUBLISHED),
            )
        )
        if not _can_moderate(request.user):
            queryset = queryset.filter(moderation_status=Post.ModerationStatus.PUBLISHED)

        kind = request.GET.get("kind")
        if kind:
            queryset = queryset.filter(kind=kind)

        author_id = request.GET.get("author_id")
        if author_id:
            queryset = queryset.filter(author_id=author_id)

        posts = [serialize_post(post) for post in queryset[:50]]
        return JsonResponse({"count": len(posts), "results": posts})

    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)

    try:
        payload = _parse_json_body(request)
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    title = str(payload.get("title", "")).strip()
    body = str(payload.get("body", "")).strip()
    if not title or not body:
        return JsonResponse({"detail": "Both title and body are required."}, status=400)

    kind = payload.get("kind") or Post.PostType.UPDATE
    visibility = payload.get("visibility") or Post.Visibility.COMPANY
    can_publish = _can_publish(request.user)
    post = Post.objects.create(
        author=request.user,
        title=title,
        body=body,
        kind=kind,
        visibility=visibility,
        allow_comments=bool(payload.get("allow_comments", True)),
        moderation_status=(
            Post.ModerationStatus.PUBLISHED
            if can_publish
            else Post.ModerationStatus.PENDING_REVIEW
        ),
        published_at=timezone.now() if can_publish else None,
    )
    record_audit_event(
        action="post.created",
        actor=request.user,
        target=post,
        summary=f"Created post '{post.title}'",
        metadata={"kind": post.kind, "visibility": post.visibility},
        request=request,
    )
    record_analytics_event(
        "feed",
        "post_created",
        actor=request.user,
        metadata={"post_id": post.id, "moderation_status": post.moderation_status},
        request=request,
    )
    return JsonResponse({"post": serialize_post(post)}, status=201)


@csrf_exempt
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

    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)
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
