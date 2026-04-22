from django.urls import path

from .views import (
    analytics_ingest,
    analytics_recent,
    audit_log_feed,
    celebration_candidates_today,
    celebration_preview,
    celebration_publish,
    healthcheck,
    moderate_comment,
    moderate_post,
    moderation_queue,
    ops_summary,
    reported_error_detail,
    reported_errors_collection,
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
    path("reported-errors/", reported_errors_collection, name="reported-errors-collection"),
    path("reported-errors/<int:reported_error_id>/", reported_error_detail, name="reported-error-detail"),
    path("celebrations/today/", celebration_candidates_today, name="celebration-candidates-today"),
    path("celebrations/preview/", celebration_preview, name="celebration-preview"),
    path("celebrations/publish/", celebration_publish, name="celebration-publish"),
]
