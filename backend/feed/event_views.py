import json

from django.db.models import Count, Q
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from operations.services import record_analytics_event, record_audit_event

from .models import Comment, Post, PostReaction
from .serializers import serialize_post

EVENTS_TOPIC = "connect_events"


def _parse_json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Request body must be valid JSON.") from exc


def _query_limit(request, default=50, maximum=200):
    raw_value = str(request.GET.get("limit", "")).strip()
    if not raw_value:
        return default
    try:
        parsed = int(raw_value)
    except (TypeError, ValueError):
        return default
    if parsed < 1:
        return default
    return min(parsed, maximum)


def _can_manage_events(user):
    return user.is_authenticated and (
        getattr(user, "can_administer_connect", False)
        or user.is_staff
        or user.has_perm("feed.publish_post")
    )


def _events_queryset():
    return (
        Post.objects.select_related("author")
        .annotate(
            published_comment_count=Count(
                "comments",
                filter=Q(comments__moderation_status=Comment.ModerationStatus.PUBLISHED),
                distinct=True,
            ),
            like_reaction_count=Count(
                "reactions",
                filter=Q(reactions__reaction_type=PostReaction.ReactionType.LIKE),
                distinct=True,
            ),
        )
        .filter(module=Post.Module.BULLETIN, topic=EVENTS_TOPIC)
        .exclude(moderation_status=Post.ModerationStatus.REMOVED)
    )


def _normalize_event_metadata(metadata):
    if not isinstance(metadata, dict):
        return None
    return {
        **metadata,
        "post_as_company": True,
        "bulletin_category": "events",
        "event_post": True,
    }


def _requested_status(payload, default=Post.ModerationStatus.PUBLISHED):
    status = str(payload.get("moderation_status") or default).strip().lower()
    if status not in {Post.ModerationStatus.DRAFT, Post.ModerationStatus.PUBLISHED}:
        return None
    return status


def _validate_post_type(payload):
    kind = str(payload.get("kind") or Post.PostType.ANNOUNCEMENT).strip()
    if kind not in Post.PostType.values:
        return None
    return kind


def _validate_visibility(payload):
    visibility = str(payload.get("visibility") or Post.Visibility.COMPANY).strip()
    if visibility not in Post.Visibility.values:
        return None
    return visibility


def events_collection(request):
    if request.method == "GET":
        queryset = _events_queryset()
        if not _can_manage_events(request.user):
            queryset = queryset.filter(moderation_status=Post.ModerationStatus.PUBLISHED)
        limit = _query_limit(request, default=100)
        posts = [serialize_post(post, viewer=request.user) for post in queryset[:limit]]
        return JsonResponse({"count": len(posts), "results": posts})

    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])
    if not _can_manage_events(request.user):
        return JsonResponse({"detail": "Admin access is required to manage events."}, status=403)

    try:
        payload = _parse_json_body(request)
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    title = str(payload.get("title", "")).strip()
    body = str(payload.get("body", "")).strip()
    if not title or not body:
        return JsonResponse({"detail": "Both title and body are required."}, status=400)

    kind = _validate_post_type(payload)
    if not kind:
        return JsonResponse({"detail": "Invalid kind supplied."}, status=400)

    visibility = _validate_visibility(payload)
    if not visibility:
        return JsonResponse({"detail": "Invalid visibility supplied."}, status=400)

    metadata = _normalize_event_metadata(payload.get("metadata") or {})
    if metadata is None:
        return JsonResponse({"detail": "Metadata must be a JSON object."}, status=400)

    moderation_status = _requested_status(payload)
    if not moderation_status:
        return JsonResponse({"detail": "Unsupported moderation status."}, status=400)

    post = Post.objects.create(
        author=request.user,
        title=title,
        body=body,
        kind=kind,
        module=Post.Module.BULLETIN,
        topic=EVENTS_TOPIC,
        metadata=metadata,
        visibility=visibility,
        allow_comments=bool(payload.get("allow_comments", False)),
        pinned=False,
        moderation_status=moderation_status,
        published_at=timezone.now() if moderation_status == Post.ModerationStatus.PUBLISHED else None,
    )
    record_audit_event(
        action="event.created",
        actor=request.user,
        target=post,
        summary=f"Created event '{post.title}'",
        metadata={"post_id": post.id, "moderation_status": post.moderation_status},
        request=request,
    )
    record_analytics_event(
        "events",
        "event_created",
        actor=request.user,
        metadata={"post_id": post.id, "moderation_status": post.moderation_status},
        request=request,
    )
    return JsonResponse({"post": serialize_post(post, viewer=request.user)}, status=201)


def event_detail(request, post_id):
    if request.method not in {"PATCH", "DELETE"}:
        return HttpResponseNotAllowed(["PATCH", "DELETE"])
    if not _can_manage_events(request.user):
        return JsonResponse({"detail": "Admin access is required to manage events."}, status=403)

    post = get_object_or_404(_events_queryset(), pk=post_id)

    if request.method == "DELETE":
        post.moderation_status = Post.ModerationStatus.REMOVED
        post.pinned = False
        post.save(update_fields=["moderation_status", "pinned", "updated_at"])
        record_audit_event(
            action="event.deleted",
            actor=request.user,
            target=post,
            summary=f"Deleted event '{post.title}'",
            metadata={"post_id": post.id},
            request=request,
        )
        record_analytics_event(
            "events",
            "event_deleted",
            actor=request.user,
            metadata={"post_id": post.id},
            request=request,
        )
        return JsonResponse({"detail": "Event deleted successfully.", "post_id": post.id})

    try:
        payload = _parse_json_body(request)
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    update_fields = ["updated_at"]
    if "title" in payload:
        title = str(payload.get("title", "")).strip()
        if not title:
            return JsonResponse({"detail": "Title is required."}, status=400)
        post.title = title
        update_fields.append("title")

    if "body" in payload:
        body = str(payload.get("body", "")).strip()
        if not body:
            return JsonResponse({"detail": "Body is required."}, status=400)
        post.body = body
        update_fields.append("body")

    if "kind" in payload:
        kind = _validate_post_type(payload)
        if not kind:
            return JsonResponse({"detail": "Invalid kind supplied."}, status=400)
        post.kind = kind
        update_fields.append("kind")

    if "visibility" in payload:
        visibility = _validate_visibility(payload)
        if not visibility:
            return JsonResponse({"detail": "Invalid visibility supplied."}, status=400)
        post.visibility = visibility
        update_fields.append("visibility")

    if "metadata" in payload:
        metadata = _normalize_event_metadata(payload.get("metadata") or {})
        if metadata is None:
            return JsonResponse({"detail": "Metadata must be a JSON object."}, status=400)
        post.metadata = metadata
        update_fields.append("metadata")

    if "allow_comments" in payload:
        post.allow_comments = bool(payload.get("allow_comments"))
        update_fields.append("allow_comments")

    if "moderation_status" in payload:
        moderation_status = _requested_status(payload, default=post.moderation_status)
        if not moderation_status:
            return JsonResponse({"detail": "Unsupported moderation status."}, status=400)
        post.moderation_status = moderation_status
        post.pinned = False
        update_fields.extend(["moderation_status", "pinned"])
        if moderation_status == Post.ModerationStatus.PUBLISHED:
            post.published_at = post.published_at or timezone.now()
        else:
            post.published_at = None
        update_fields.append("published_at")

    if update_fields == ["updated_at"]:
        return JsonResponse({"detail": "No supported fields supplied."}, status=400)

    post.save(update_fields=sorted(set(update_fields)))
    record_audit_event(
        action="event.updated",
        actor=request.user,
        target=post,
        summary=f"Updated event '{post.title}'",
        metadata={"post_id": post.id, "moderation_status": post.moderation_status},
        request=request,
    )
    record_analytics_event(
        "events",
        "event_updated",
        actor=request.user,
        metadata={"post_id": post.id, "moderation_status": post.moderation_status},
        request=request,
    )
    post = get_object_or_404(_events_queryset(), pk=post_id)
    return JsonResponse({"post": serialize_post(post, viewer=request.user)})
