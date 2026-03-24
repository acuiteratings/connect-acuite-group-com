from __future__ import annotations

from datetime import date
import calendar

from accounts.models import User
from directory.models import DirectoryProfile
from django.db import models
from feed.models import Comment, Post, PostReaction

POINT_RULES = {
    "published_post": 10,
    "published_comment": 3,
    "reaction_given": 1,
    "reaction_received": 2,
}


def _safe_anniversary_date(year: int, month: int, day: int) -> date:
    last_day = calendar.monthrange(year, month)[1]
    return date(year, month, min(day, last_day))


def _next_annual_occurrence(month: int, day: int, reference_date: date) -> date:
    current_year_target = _safe_anniversary_date(reference_date.year, month, day)
    if current_year_target < reference_date:
        return _safe_anniversary_date(reference_date.year + 1, month, day)
    return current_year_target


def _format_upcoming_label(target_date: date, reference_date: date) -> str:
    if target_date == reference_date:
        return "Today"
    return target_date.strftime("%d %b")


def _active_profiles_queryset():
    return DirectoryProfile.objects.select_related("user").filter(
        user__is_active=True,
        is_visible=True,
        user__is_directory_visible=True,
    )


def build_points_table():
    eligible_users = {
        user.id: {
            "user_id": user.id,
            "name": user.full_name,
            "initials": user.initials,
            "title": user.title,
            "location": user.location,
            "points": 0,
            "breakdown": {
                "published_post": 0,
                "published_comment": 0,
                "reaction_given": 0,
                "reaction_received": 0,
            },
        }
        for user in User.objects.filter(
            is_active=True,
            employment_status=User.EmploymentStatus.ACTIVE,
        )
    }

    for row in (
        Post.objects.filter(moderation_status=Post.ModerationStatus.PUBLISHED)
        .values("author_id")
        .order_by()
        .annotate(count=models.Count("id"))
    ):
        if row["author_id"] in eligible_users:
            eligible_users[row["author_id"]]["breakdown"]["published_post"] = row["count"]

    for row in (
        Comment.objects.filter(moderation_status=Comment.ModerationStatus.PUBLISHED)
        .values("author_id")
        .order_by()
        .annotate(count=models.Count("id"))
    ):
        if row["author_id"] in eligible_users:
            eligible_users[row["author_id"]]["breakdown"]["published_comment"] = row["count"]

    for row in (
        PostReaction.objects.filter(reaction_type=PostReaction.ReactionType.LIKE)
        .values("user_id")
        .order_by()
        .annotate(count=models.Count("id"))
    ):
        if row["user_id"] in eligible_users:
            eligible_users[row["user_id"]]["breakdown"]["reaction_given"] = row["count"]

    for row in (
        PostReaction.objects.filter(reaction_type=PostReaction.ReactionType.LIKE)
        .values("post__author_id")
        .order_by()
        .annotate(count=models.Count("id"))
    ):
        author_id = row["post__author_id"]
        if author_id in eligible_users:
            eligible_users[author_id]["breakdown"]["reaction_received"] = row["count"]

    rows = []
    for item in eligible_users.values():
        points = sum(
            POINT_RULES[key] * item["breakdown"][key]
            for key in item["breakdown"]
        )
        item["points"] = points
        rows.append(item)

    rows.sort(key=lambda item: (-item["points"], item["name"].lower()))
    return rows


def build_birthdays(limit=5):
    today = date.today()
    items = []
    for profile in _active_profiles_queryset().exclude(date_of_birth__isnull=True):
        next_date = _next_annual_occurrence(
            profile.date_of_birth.month,
            profile.date_of_birth.day,
            today,
        )
        items.append(
            {
                "id": profile.user_id,
                "name": profile.user.full_name,
                "initials": profile.user.initials,
                "title": profile.user.title,
                "date_label": _format_upcoming_label(next_date, today),
                "highlight": next_date == today,
                "next_date": next_date,
            }
        )

    items.sort(key=lambda item: (item["next_date"], item["name"].lower()))
    return [
        {key: value for key, value in item.items() if key != "next_date"}
        for item in items[:limit]
    ]


def build_anniversaries(limit=5):
    today = date.today()
    items = []
    for profile in _active_profiles_queryset().exclude(joined_on__isnull=True):
        next_date = _next_annual_occurrence(
            profile.joined_on.month,
            profile.joined_on.day,
            today,
        )
        years = next_date.year - profile.joined_on.year
        items.append(
            {
                "id": profile.user_id,
                "name": profile.user.full_name,
                "initials": profile.user.initials,
                "title": profile.user.title,
                "date_label": _format_upcoming_label(next_date, today),
                "years": years,
                "highlight": next_date == today,
                "next_date": next_date,
            }
        )

    items.sort(key=lambda item: (item["next_date"], item["name"].lower()))
    return [
        {key: value for key, value in item.items() if key != "next_date"}
        for item in items[:limit]
    ]


def build_recognition_overview(for_user):
    points_table = build_points_table()
    my_points = 0
    if getattr(for_user, "is_authenticated", False):
        match = next((row for row in points_table if row["user_id"] == for_user.id), None)
        if match:
            my_points = match["points"]

    recognition_posts = Post.objects.filter(
        module=Post.Module.RECOGNITION,
        moderation_status=Post.ModerationStatus.PUBLISHED,
    )
    kudos_count = recognition_posts.filter(topic="kudos").count()
    milestone_count = recognition_posts.filter(topic="milestone").count()

    return {
        "current_user_points": my_points,
        "point_rules": [
            {"key": key, "points": points}
            for key, points in POINT_RULES.items()
        ],
        "leaderboard": points_table[:5],
        "birthdays": build_birthdays(),
        "anniversaries": build_anniversaries(),
        "totals": {
            "recognition_posts": recognition_posts.count(),
            "kudos_posts": kudos_count,
            "milestone_posts": milestone_count,
        },
    }
