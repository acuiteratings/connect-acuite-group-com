from datetime import date

from django.utils import timezone

from accounts.serializers import serialize_user

from .models import Comment, PostReaction


MEDICLAIM_NOTICE_START_DATE = date(2026, 6, 3)
MEDICLAIM_NOTICE_REVERT_DATE = date(2026, 6, 5)
MEDICLAIM_NOTICE_TITLE = "Mediclaim Policy Orientation Session"
MEDICLAIM_NOTICE_TEAMS_LINK = (
    "https://teams.microsoft.com/meet/47123779931799?p=ofNdg3rsrsalS0dj1O"
)
MEDICLAIM_NOTICE_BODY = (
    "A Mediclaim Policy Orientation Session is scheduled with our insurance brokers for the "
    "policy period 18 April 2026 to 17 April 2027.\n\n"
    "During this session, a comprehensive overview of the Mediclaim policy will be given and "
    "any questions you may have will be addressed.\n\n"
    "To help you access policy-related services conveniently, all are requested to download the "
    "Loop Health mobile application prior to the session.\n\n"
    f"Join: {MEDICLAIM_NOTICE_TEAMS_LINK}\n"
    "Meeting ID: 471 237 799 317 99\n"
    "Passcode: ry92FY6P"
)
MEDICLAIM_NOTICE_SUMMARY = (
    "A Mediclaim Policy Orientation Session is scheduled with our insurance brokers for the "
    "policy period 18 April 2026 to 17 April 2027."
)
MEDICLAIM_NOTICE_DETAILS = [
    "Session Details:",
    "Date: 4 June 2026",
    "Time: 4:30 PM",
    "Platform: Microsoft Teams",
    (
        "During this session, a comprehensive overview of the Mediclaim policy will be given "
        "and any questions you may have will be addressed."
    ),
    (
        "Please download the Loop Health mobile application prior to the session to access "
        "policy-related services conveniently."
    ),
    f"Join: {MEDICLAIM_NOTICE_TEAMS_LINK}",
    "Meeting ID: 471 237 799 317 99",
    "Passcode: ry92FY6P",
]


def _is_people_culture_announcement(post):
    metadata = post.metadata or {}
    return (
        str(metadata.get("home_announcement_tag", "")).strip().lower() == "people_culture"
        and post.module == "bulletin"
        and post.topic == "announcements"
    )


def is_mediclaim_notice_active(post, *, today=None):
    today = today or timezone.localdate()
    return (
        _is_people_culture_announcement(post)
        and MEDICLAIM_NOTICE_START_DATE <= today < MEDICLAIM_NOTICE_REVERT_DATE
    )


def _mediclaim_notice_metadata(metadata):
    return {
        **metadata,
        "bulletin_meta_lines": ["4 June 2026 | 4:30 PM | Microsoft Teams"],
        "home_announcement_display": {
            "formatLabel": "Orientation",
            "dateLabel": "4 June 2026",
            "timeLabel": "4:30 PM",
            "venueLabel": "Microsoft Teams",
            "hostLabel": "People & Culture",
            "audienceLabel": "For all employees",
            "countdownLabel": "Policy period: 18 April 2026 to 17 April 2027",
            "summary": MEDICLAIM_NOTICE_SUMMARY,
            "details": MEDICLAIM_NOTICE_DETAILS,
            "ctaLabel": "Join on Microsoft Teams",
            "ctaTarget": MEDICLAIM_NOTICE_TEAMS_LINK,
        },
        "bulletin_cta_label": "Join on Microsoft Teams",
        "bulletin_cta_target": MEDICLAIM_NOTICE_TEAMS_LINK,
        "post_as_company": True,
        "company_author_name": "People & Culture",
        "company_author_title": "Official company post",
        "company_author_initials": "PC",
    }


def serialize_post(post, *, viewer=None):
    metadata = post.metadata or {}
    mediclaim_notice_active = is_mediclaim_notice_active(post)
    if mediclaim_notice_active:
        metadata = _mediclaim_notice_metadata(metadata)
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
    if mediclaim_notice_active:
        reaction_count = 0
        current_user_has_reacted = False
    return {
        "id": post.id,
        "title": MEDICLAIM_NOTICE_TITLE if mediclaim_notice_active else post.title,
        "body": MEDICLAIM_NOTICE_BODY if mediclaim_notice_active else post.body,
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
