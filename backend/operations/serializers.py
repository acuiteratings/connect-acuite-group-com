from .models import AnalyticsEvent, ErrorEvent, ReportedError


def serialize_audit_log(log):
    return {
        "id": log.id,
        "action": log.action,
        "summary": log.summary,
        "request_id": log.request_id,
        "actor": log.actor.full_name if log.actor else None,
        "actor_email": log.actor.email if log.actor else None,
        "target_type": log.target_content_type.model if log.target_content_type else None,
        "target_object_id": log.target_object_id,
        "metadata": log.metadata,
        "ip_address": log.ip_address,
        "created_at": log.created_at.isoformat(),
    }


def serialize_analytics_event(event):
    return {
        "id": event.id,
        "category": event.category,
        "event_name": event.event_name,
        "request_id": event.request_id,
        "path": event.path,
        "metadata": event.metadata,
        "actor": event.actor.full_name if event.actor else None,
        "actor_email": event.actor.email if event.actor else None,
        "ip_address": event.ip_address,
        "occurred_at": event.occurred_at.isoformat(),
    }


def serialize_error_event(event):
    return {
        "id": event.id,
        "request_id": event.request_id,
        "path": event.path,
        "method": event.method,
        "status_code": event.status_code,
        "exception_type": event.exception_type,
        "message": event.message,
        "metadata": event.metadata,
        "is_resolved": event.is_resolved,
        "resolved_at": event.resolved_at.isoformat() if event.resolved_at else None,
        "actor": event.actor.full_name if event.actor else None,
        "actor_email": event.actor.email if event.actor else None,
        "occurred_at": event.occurred_at.isoformat(),
    }


def serialize_reported_error(event):
    return {
        "id": event.id,
        "title": event.title,
        "details": event.details,
        "source_tab": event.source_tab,
        "page_path": event.page_path,
        "metadata": event.metadata,
        "reporter": event.reporter.full_name if event.reporter else None,
        "reporter_email": event.reporter.email if event.reporter else None,
        "created_at": event.created_at.isoformat(),
    }


def moderation_counts_payload(pending_posts, pending_comments):
    return {
        "pending_posts": pending_posts,
        "pending_comments": pending_comments,
        "total_pending": pending_posts + pending_comments,
    }
