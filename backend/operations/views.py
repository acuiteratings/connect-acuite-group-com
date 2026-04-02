import json
from datetime import timedelta

from django.conf import settings
from django.db.models import Count, Q
from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from accounts.models import User
from directory.models import DirectoryProfile
from feed.models import Comment, Post
from feed.serializers import serialize_comment, serialize_post

from .models import AnalyticsEvent, AuditLog, ErrorEvent
from .celebrations import (
    build_celebration_preview,
    get_today_celebration_candidates,
    publish_celebration_post_from_preview,
)
from .serializers import (
    moderation_counts_payload,
    serialize_analytics_event,
    serialize_audit_log,
    serialize_error_event,
)
from .services import record_analytics_event, record_audit_event


def _parse_json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Request body must be valid JSON.") from exc


def _is_ops_user(user):
    return user.is_authenticated and (
        user.is_staff
        or getattr(user, "access_level", "") in {User.AccessLevel.MODERATOR, User.AccessLevel.ADMIN}
        or user.has_perm("feed.moderate_post")
        or user.has_perm("feed.moderate_comment")
    )


def _forbidden(detail="Moderation access required."):
    return JsonResponse({"detail": detail}, status=403)


def _is_admin_user(user):
    return user.is_authenticated and (
        user.is_staff
        or getattr(user, "can_administer_connect", False)
        or getattr(user, "access_level", "") == User.AccessLevel.ADMIN
        or user.has_perm("accounts.manage_access_rights")
    )


def _moderation_counts():
    pending_posts = Post.objects.filter(
        moderation_status=Post.ModerationStatus.PENDING_REVIEW
    ).count()
    pending_comments = Comment.objects.filter(
        moderation_status=Comment.ModerationStatus.PENDING_REVIEW
    ).count()
    return moderation_counts_payload(pending_posts, pending_comments)


def _decision_label(decision):
    return {
        "publish": "Published",
        "reject": "Rejected",
        "remove": "Removed",
    }[decision]


def _publish_post(post):
    post.publish()


def _apply_post_decision(post, decision):
    if decision == "publish":
        _publish_post(post)
    elif decision == "reject":
        post.moderation_status = Post.ModerationStatus.REJECTED
        post.save(update_fields=["moderation_status", "updated_at"])
    elif decision == "remove":
        post.moderation_status = Post.ModerationStatus.REMOVED
        post.save(update_fields=["moderation_status", "updated_at"])
    else:
        raise ValueError("Decision must be one of: publish, reject, remove.")


def _apply_comment_decision(comment, decision):
    if decision == "publish":
        comment.moderation_status = Comment.ModerationStatus.PUBLISHED
    elif decision == "reject":
        comment.moderation_status = Comment.ModerationStatus.REJECTED
    elif decision == "remove":
        comment.moderation_status = Comment.ModerationStatus.REMOVED
    else:
        raise ValueError("Decision must be one of: publish, reject, remove.")
    comment.save(update_fields=["moderation_status", "updated_at"])


def healthcheck(request):
    return JsonResponse(
        {
            "status": "ok",
            "service": "acuite-connect-backend",
            "time": timezone.now().isoformat(),
            "request_id": getattr(request, "request_id", ""),
            "monitoring": {
                "sentry_enabled": bool(getattr(settings, "SENTRY_ENABLED", False)),
            },
        }
    )


def ops_summary(request):
    if not _is_ops_user(request.user):
        return _forbidden()

    since = timezone.now() - timedelta(hours=24)
    summary = {
        "users": {
            "active": User.objects.filter(
                is_active=True,
                employment_status=User.EmploymentStatus.ACTIVE,
            ).count(),
            "staff": User.objects.filter(is_staff=True).count(),
        },
        "directory": {
            "visible_profiles": DirectoryProfile.objects.filter(
                is_visible=True,
                user__is_directory_visible=True,
            ).count(),
        },
        "feed": {
            "published_posts": Post.objects.filter(
                moderation_status=Post.ModerationStatus.PUBLISHED
            ).count(),
            "published_comments": Comment.objects.filter(
                moderation_status=Comment.ModerationStatus.PUBLISHED
            ).count(),
        },
        "moderation": _moderation_counts(),
        "activity_24h": {
            "audit_events": AuditLog.objects.filter(created_at__gte=since).count(),
            "analytics_events": AnalyticsEvent.objects.filter(occurred_at__gte=since).count(),
            "errors": ErrorEvent.objects.filter(occurred_at__gte=since).count(),
        },
    }

    recent_errors = [
        serialize_error_event(event)
        for event in ErrorEvent.objects.select_related("actor")[:5]
    ]
    return JsonResponse(
        {
            "summary": summary,
            "recent_errors": recent_errors,
            "request_id": getattr(request, "request_id", ""),
        }
    )


def moderation_queue(request):
    if not _is_ops_user(request.user):
        return _forbidden()

    limit = min(int(request.GET.get("limit", 25)), 100)
    pending_posts = Post.objects.select_related("author").filter(
        moderation_status=Post.ModerationStatus.PENDING_REVIEW
    )[:limit]
    pending_comments = Comment.objects.select_related("author", "post").filter(
        moderation_status=Comment.ModerationStatus.PENDING_REVIEW
    )[:limit]

    return JsonResponse(
        {
            "counts": _moderation_counts(),
            "posts": [serialize_post(post) for post in pending_posts],
            "comments": [serialize_comment(comment) for comment in pending_comments],
        }
    )


@csrf_exempt
def moderate_post(request, post_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not _is_ops_user(request.user):
        return _forbidden()

    post = get_object_or_404(Post.objects.select_related("author"), pk=post_id)
    try:
        payload = _parse_json_body(request)
        decision = str(payload.get("decision", "")).strip().lower()
        note = str(payload.get("note", "")).strip()
        _apply_post_decision(post, decision)
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    record_audit_event(
        action=f"moderation.post.{decision}",
        actor=request.user,
        target=post,
        summary=f"{_decision_label(decision)} post '{post.title}'",
        metadata={"decision": decision, "note": note},
        request=request,
    )
    record_analytics_event(
        "moderation",
        f"post_{decision}",
        actor=request.user,
        metadata={"post_id": post.id, "note_present": bool(note)},
        request=request,
    )
    return JsonResponse({"post": serialize_post(post), "counts": _moderation_counts()})


@csrf_exempt
def moderate_comment(request, comment_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not _is_ops_user(request.user):
        return _forbidden()

    comment = get_object_or_404(Comment.objects.select_related("author", "post"), pk=comment_id)
    try:
        payload = _parse_json_body(request)
        decision = str(payload.get("decision", "")).strip().lower()
        note = str(payload.get("note", "")).strip()
        _apply_comment_decision(comment, decision)
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    record_audit_event(
        action=f"moderation.comment.{decision}",
        actor=request.user,
        target=comment,
        summary=f"{_decision_label(decision)} comment on '{comment.post.title}'",
        metadata={"decision": decision, "note": note, "post_id": comment.post_id},
        request=request,
    )
    record_analytics_event(
        "moderation",
        f"comment_{decision}",
        actor=request.user,
        metadata={"comment_id": comment.id, "post_id": comment.post_id, "note_present": bool(note)},
        request=request,
    )
    return JsonResponse({"comment": serialize_comment(comment), "counts": _moderation_counts()})


def audit_log_feed(request):
    if not _is_ops_user(request.user):
        return _forbidden()

    limit = min(int(request.GET.get("limit", 50)), 100)
    queryset = AuditLog.objects.select_related("actor", "target_content_type")
    action = request.GET.get("action")
    if action:
        queryset = queryset.filter(action=action)
    results = [serialize_audit_log(log) for log in queryset[:limit]]
    return JsonResponse({"count": len(results), "results": results})


def recent_errors(request):
    if not _is_ops_user(request.user):
        return _forbidden()

    include_resolved = request.GET.get("include_resolved") == "true"
    queryset = ErrorEvent.objects.select_related("actor")
    if not include_resolved:
        queryset = queryset.filter(is_resolved=False)
    results = [serialize_error_event(event) for event in queryset[:50]]
    return JsonResponse({"count": len(results), "results": results})


def analytics_recent(request):
    if not _is_ops_user(request.user):
        return _forbidden()

    limit = min(int(request.GET.get("limit", 50)), 100)
    queryset = AnalyticsEvent.objects.select_related("actor")
    category = request.GET.get("category")
    if category:
        queryset = queryset.filter(category=category)
    results = [serialize_analytics_event(event) for event in queryset[:limit]]
    return JsonResponse({"count": len(results), "results": results})


def celebration_candidates_today(request):
    if not _is_admin_user(request.user):
        return _forbidden("Admin access required.")
    return JsonResponse(get_today_celebration_candidates())


@csrf_exempt
def celebration_preview(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not _is_admin_user(request.user):
        return _forbidden("Admin access required.")
    try:
        payload = _parse_json_body(request)
        kind = str(payload.get("kind", "")).strip().lower()
        user_id = int(payload.get("user_id") or 0)
        template_name = str(payload.get("template_file", "")).strip()
        preview = build_celebration_preview(
            kind=kind,
            user_id=user_id,
            template_name=template_name,
        )
    except (ValueError, DirectoryProfile.DoesNotExist) as exc:
        return JsonResponse({"detail": str(exc) or "Could not build the preview."}, status=400)
    except RuntimeError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)
    return JsonResponse({"preview": preview})


@csrf_exempt
def celebration_publish(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not _is_admin_user(request.user):
        return _forbidden("Admin access required.")
    try:
        payload = _parse_json_body(request)
        kind = str(payload.get("kind", "")).strip().lower()
        user_id = int(payload.get("user_id") or 0)
        template_name = str(payload.get("template_file", "")).strip()
        if not template_name:
            raise ValueError("Template file is required.")
        post = publish_celebration_post_from_preview(
            kind=kind,
            user_id=user_id,
            template_name=template_name,
        )
    except (ValueError, DirectoryProfile.DoesNotExist) as exc:
        return JsonResponse({"detail": str(exc) or "Could not publish the celebration post."}, status=400)
    except RuntimeError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)
    return JsonResponse({"post": serialize_post(post, viewer=request.user)}, status=201)


@csrf_exempt
def analytics_ingest(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    try:
        payload = _parse_json_body(request)
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    category = str(payload.get("category", "")).strip().lower()
    event_name = str(payload.get("event_name", "")).strip().lower()
    if not category or not event_name:
        return JsonResponse({"detail": "Both category and event_name are required."}, status=400)

    metadata = payload.get("metadata") if isinstance(payload.get("metadata"), dict) else {}
    event = record_analytics_event(
        category,
        event_name,
        actor=request.user,
        path=str(payload.get("path", "")).strip(),
        metadata=metadata,
        request=request,
    )
    return JsonResponse(
        {
            "event": serialize_analytics_event(event),
            "request_id": getattr(request, "request_id", ""),
        },
        status=201,
    )
