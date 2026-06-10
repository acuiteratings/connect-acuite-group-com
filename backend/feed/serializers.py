from datetime import date

from django.utils import timezone

from accounts.serializers import serialize_user

from .models import Comment, PostReaction


PEOPLE_CULTURE_ADVISORY_START_DATE = date(2026, 6, 10)
PEOPLE_CULTURE_ADVISORY_REVERT_DATE = date(2026, 6, 21)
PEOPLE_CULTURE_ADVISORY_TITLE = "HR Advisory - EPFO Account Details"
PEOPLE_CULTURE_ADVISORY_LINK = "https://unifiedportal-mem.epfindia.gov.in/memberinterface/"
PEOPLE_CULTURE_ADVISORY_BODY = (
    "Are your EPFO details updated?\n\n"
    f"Please log in to the EPFO website {PEOPLE_CULTURE_ADVISORY_LINK} to check if:\n"
    "- Your UAN is active (UAN is available on your salary slips)\n"
    "- Your KYC is updated\n"
    "- Your mobile number is correct and updated so that you get the OTP and other details on your phone.\n"
    "- Your mandatory e-nomination is submitted.\n\n"
    "Please ensure to activate your UAN and update your KYC online to have hassle free PF transfers/claim processing. "
    "Also please ensure that your e-nomination details are up to date. This is essential to safeguard the financial "
    "interests of your loved ones and ensure a seamless process in case of unforeseen circumstances.\n\n"
    "Should you need any assistance, please feel free to reach out to the HR team."
)
PEOPLE_CULTURE_ADVISORY_SUMMARY = "Are your EPFO details updated?"
PEOPLE_CULTURE_ADVISORY_DETAILS = [
    f"Please log in to the EPFO website to review the items below: {PEOPLE_CULTURE_ADVISORY_LINK}",
    (
        "Please ensure to activate your UAN and update your KYC online to have hassle free PF transfers/claim processing."
    ),
    (
        "Please also ensure that your e-nomination details are up to date. This is essential to safeguard the financial "
        "interests of your loved ones and ensure a seamless process in case of unforeseen circumstances."
    ),
]
PEOPLE_CULTURE_ADVISORY_CHECKLIST = [
    "Your UAN is active (UAN is available on your salary slips)",
    "Your KYC is updated",
    "Your mobile number is correct and updated so that you get the OTP and other details on your phone.",
    "Your mandatory e-nomination is submitted.",
]


def _is_people_culture_announcement(post):
    metadata = post.metadata or {}
    return (
        str(metadata.get("home_announcement_tag", "")).strip().lower() == "people_culture"
        and post.module == "bulletin"
        and post.topic == "announcements"
    )


def is_people_culture_advisory_active(post, *, today=None):
    today = today or timezone.localdate()
    return (
        _is_people_culture_announcement(post)
        and PEOPLE_CULTURE_ADVISORY_START_DATE <= today < PEOPLE_CULTURE_ADVISORY_REVERT_DATE
    )


def _people_culture_advisory_metadata(metadata):
    return {
        **metadata,
        "bulletin_meta_lines": ["Until 20 June 2026 | EPFO Member Portal | HR Team"],
        "home_announcement_display": {
            "formatLabel": "HR Advisory",
            "dateLabel": "Until 20 June 2026",
            "timeLabel": "Action this week",
            "venueLabel": "EPFO Member Portal",
            "hostLabel": "HR Team",
            "audienceLabel": "For all employees",
            "countdownLabel": "Please verify UAN, KYC, mobile number, and e-nomination",
            "summary": PEOPLE_CULTURE_ADVISORY_SUMMARY,
            "details": PEOPLE_CULTURE_ADVISORY_DETAILS,
            "layoutVariant": "advisory_checklist",
            "checklistItems": PEOPLE_CULTURE_ADVISORY_CHECKLIST,
            "closingNote": "Should you need any assistance, please feel free to reach out to the HR team.",
            "ctaLabel": "Open EPFO website",
            "ctaTarget": PEOPLE_CULTURE_ADVISORY_LINK,
        },
        "bulletin_cta_label": "Open EPFO website",
        "bulletin_cta_target": PEOPLE_CULTURE_ADVISORY_LINK,
        "post_as_company": True,
        "company_author_name": "HR",
        "company_author_title": "Official company post",
        "company_author_initials": "HR",
    }


def serialize_post(post, *, viewer=None):
    metadata = post.metadata or {}
    people_culture_advisory_active = is_people_culture_advisory_active(post)
    if people_culture_advisory_active:
        metadata = _people_culture_advisory_metadata(metadata)
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
    if people_culture_advisory_active:
        reaction_count = 0
        current_user_has_reacted = False
    return {
        "id": post.id,
        "title": PEOPLE_CULTURE_ADVISORY_TITLE if people_culture_advisory_active else post.title,
        "body": PEOPLE_CULTURE_ADVISORY_BODY if people_culture_advisory_active else post.body,
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
