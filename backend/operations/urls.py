from django.urls import path

from .views import (
    analytics_ingest,
    analytics_recent,
    audit_log_feed,
    healthcheck,
    moderate_comment,
    moderate_post,
    moderation_queue,
    ops_summary,
    recent_errors,
)

urlpatterns = [
    path("health/", healthcheck, name="healthcheck"),
    path("summary/", ops_summary, name="ops-summary"),
    path("moderation/queue/", moderation_queue, name="moderation-queue"),
    path("moderation/posts/<int:post_id>/decision/", moderate_post, name="moderate-post"),
    path(
        "moderation/comments/<int:comment_id>/decision/",
        moderate_comment,
        name="moderate-comment",
    ),
    path("audit/", audit_log_feed, name="audit-log-feed"),
    path("analytics/", analytics_recent, name="analytics-recent"),
    path("analytics/ingest/", analytics_ingest, name="analytics-ingest"),
    path("errors/", recent_errors, name="recent-errors"),
]
