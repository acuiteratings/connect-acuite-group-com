from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from django.db import models
from django.utils import timezone

from accounts.models import User
from directory.models import DirectoryProfile
from feed.models import Post

from .services import record_analytics_event, record_audit_event

TEMPLATE_ROOT = Path(__file__).resolve().parent / "bulletin_templates"


@dataclass(frozen=True)
class CelebrationCandidate:
    profile: DirectoryProfile
    template_key: str
    auto_key: str
    title: str
    body: str
    meta_lines: list[str]
    occasion_date_label: str
    source_date: date


def _candidate_payload(candidate: CelebrationCandidate) -> dict:
    profile = candidate.profile
    user = profile.user
    years_completed = ""
    if candidate.template_key == "work_anniversary" and profile.joined_on:
        completed = max(candidate.source_date.year - profile.joined_on.year, 0)
        years_completed = str(completed) if completed else ""
    return {
        "user_id": user.id,
        "email": user.email,
        "name": user.full_name,
        "title": user.title,
        "department": user.department,
        "team_label": user.department or profile.company_name,
        "date_label": candidate.occasion_date_label,
        "template_key": candidate.template_key,
        "auto_key": candidate.auto_key,
        "years_completed": years_completed,
        "photo_url": _profile_photo_url(profile),
    }


def _format_display_date(value: date) -> str:
    return f"{value.day} {value.strftime('%B %Y')}"


def _template_paths(kind: str) -> list[Path]:
    folder = TEMPLATE_ROOT / kind
    return sorted(folder.glob("*.html"))


def _select_template(kind: str, *, user_id: int, reference_date: date) -> Path:
    templates = _template_paths(kind)
    if not templates:
        raise RuntimeError(f"No {kind} templates are available.")
    seed = f"{kind}:{reference_date.isoformat()}:{user_id}"
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    index = int(digest[:8], 16) % len(templates)
    return templates[index]


def _active_profiles_for_date(reference_date: date, *, kind: str):
    queryset = DirectoryProfile.objects.select_related("user").filter(
        user__is_active=True,
        user__employment_status=User.EmploymentStatus.ACTIVE,
        is_visible=True,
        user__is_directory_visible=True,
    )
    if kind == "birthday":
        return queryset.filter(
            date_of_birth__month=reference_date.month,
            date_of_birth__day=reference_date.day,
        )
    if kind == "anniversary":
        return queryset.filter(
            joined_on__month=reference_date.month,
            joined_on__day=reference_date.day,
        )
    raise ValueError(f"Unsupported celebration kind: {kind}")


def _pick_company_author() -> User:
    author = (
        User.objects.filter(is_active=True)
        .filter(models.Q(is_superuser=True) | models.Q(access_level=User.AccessLevel.ADMIN))
        .order_by("-is_superuser", "email")
        .first()
    )
    if author:
        return author
    author = User.objects.filter(
        is_active=True,
        employment_status=User.EmploymentStatus.ACTIVE,
    ).order_by("email").first()
    if author:
        return author
    raise RuntimeError("No active user is available to author automatic celebration posts.")


def _profile_photo_url(profile: DirectoryProfile) -> str:
    photos = profile.profile_photos if isinstance(profile.profile_photos, list) else []
    for item in photos:
        text = str(item or "").strip()
        if text:
            return text
    return ""


def _initials_from_name(name: str) -> str:
    parts = [part for part in str(name or "").strip().split() if part]
    if len(parts) >= 2:
        return f"{parts[0][0]}{parts[1][0]}".upper()
    if parts:
        return parts[0][:2].upper()
    return "AC"


def _template_label(template_path: Path) -> str:
    name = template_path.stem
    name = name.replace("birthday-", "").replace("anniversary-", "")
    parts = [part for part in name.split("-") if part and not part.isdigit()]
    return " ".join(word.capitalize() for word in parts) or template_path.name


def _template_style_key(template_path: Path) -> str:
    styles = ("sunrise", "confetti", "emerald", "midnight", "pearl", "gold")
    digest = hashlib.sha256(template_path.name.encode("utf-8")).hexdigest()
    return styles[int(digest[:8], 16) % len(styles)]


def _build_celebration_card(candidate: CelebrationCandidate, *, template_path: Path) -> dict:
    profile = candidate.profile
    user = profile.user
    return {
        "style_key": _template_style_key(template_path),
        "template_label": _template_label(template_path),
        "occasion_label": "Happy Birthday" if candidate.template_key == "birthday_wish" else "Happy Work Anniversary",
        "person_name": user.full_name,
        "person_role": " | ".join(
            item for item in [user.title, user.department or profile.company_name] if item
        ),
        "date_label": candidate.occasion_date_label,
        "message": candidate.body,
        "photo_url": _profile_photo_url(profile),
        "initials": _initials_from_name(user.full_name),
    }


def _build_birthday_candidate(profile: DirectoryProfile, *, reference_date: date) -> CelebrationCandidate:
    name = profile.user.full_name
    auto_key = f"birthday:{profile.user_id}:{reference_date.isoformat()}"
    return CelebrationCandidate(
        profile=profile,
        template_key="birthday_wish",
        auto_key=auto_key,
        title=f"Birthday wishes | {name}",
        body=f"Please join us in wishing {name} a very happy birthday.",
        meta_lines=[
            item
            for item in [
                profile.user.department or profile.company_name,
                f"Birthday: {_format_display_date(reference_date)}",
            ]
            if item
        ],
        occasion_date_label=_format_display_date(reference_date),
        source_date=reference_date,
    )


def _build_anniversary_candidate(profile: DirectoryProfile, *, reference_date: date) -> CelebrationCandidate:
    name = profile.user.full_name
    joined_on = profile.joined_on or reference_date
    years_completed = max(reference_date.year - joined_on.year, 0)
    auto_key = f"work_anniversary:{profile.user_id}:{reference_date.isoformat()}"
    years_label = f"{years_completed} year" if years_completed == 1 else f"{years_completed} years"
    body = (
        f"Please join us in celebrating {name} on completing {years_label} with Acuité."
        if years_completed
        else f"Please join us in celebrating {name} on this work anniversary."
    )
    return CelebrationCandidate(
        profile=profile,
        template_key="work_anniversary",
        auto_key=auto_key,
        title=f"Work anniversary | {name}",
        body=body,
        meta_lines=[
            item
            for item in [
                years_completed and f"{years_label} completed",
                f"Date: {_format_display_date(reference_date)}",
            ]
            if item
        ],
        occasion_date_label=_format_display_date(reference_date),
        source_date=reference_date,
    )


def _build_candidate(kind: str, *, profile: DirectoryProfile, reference_date: date) -> CelebrationCandidate:
    if kind == "birthday":
        return _build_birthday_candidate(profile, reference_date=reference_date)
    if kind == "anniversary":
        return _build_anniversary_candidate(profile, reference_date=reference_date)
    raise ValueError(f"Unsupported celebration kind: {kind}")


def get_today_celebration_candidates(*, reference_date: date | None = None) -> dict:
    reference_date = reference_date or timezone.localdate()
    payload = {"reference_date": reference_date.isoformat(), "birthdays": [], "anniversaries": []}
    for kind, key in (("birthday", "birthdays"), ("anniversary", "anniversaries")):
        candidates = [
            _candidate_payload(_build_candidate(kind, profile=profile, reference_date=reference_date))
            for profile in _active_profiles_for_date(reference_date, kind=kind)
        ]
        candidates.sort(key=lambda item: item["name"].casefold())
        payload[key] = candidates
    return payload


def build_celebration_preview(*, kind: str, user_id: int, reference_date: date | None = None, template_name: str = "") -> dict:
    reference_date = reference_date or timezone.localdate()
    profile = DirectoryProfile.objects.select_related("user").get(user_id=user_id)
    candidate = _build_candidate(kind, profile=profile, reference_date=reference_date)
    if template_name:
        template_path = TEMPLATE_ROOT / ("birthday" if kind == "birthday" else "anniversary") / template_name
        if not template_path.exists():
            raise RuntimeError("Selected template file was not found.")
    else:
        template_path = _select_template(kind, user_id=user_id, reference_date=reference_date)
    card = _build_celebration_card(candidate, template_path=template_path)
    payload = _candidate_payload(candidate)
    payload.update(
        {
            "kind": kind,
            "title": candidate.title,
            "body": candidate.body,
            "meta_lines": candidate.meta_lines,
            "template_file": template_path.name,
            "template_label": card["template_label"],
            "card": card,
        }
    )
    return payload


def _existing_auto_post(auto_key: str) -> bool:
    return Post.objects.exclude(
        moderation_status=Post.ModerationStatus.REMOVED
    ).filter(metadata__bulletin_auto_key=auto_key).exists()


def _create_post_for_candidate(candidate: CelebrationCandidate, *, author: User) -> Post:
    kind = "birthday" if candidate.template_key == "birthday_wish" else "anniversary"
    template_path = _select_template(
        kind,
        user_id=candidate.profile.user_id,
        reference_date=candidate.source_date,
    )
    card = _build_celebration_card(candidate, template_path=template_path)
    metadata = {
        "post_as_company": True,
        "company_author_name": "Acuité Ratings & Research",
        "company_author_title": "Official company post",
        "company_author_initials": "AR",
        "bulletin_category": "hr",
        "bulletin_template": candidate.template_key,
        "bulletin_meta_lines": candidate.meta_lines,
        "bulletin_card": card,
        "bulletin_template_file": template_path.name,
        "bulletin_auto_key": candidate.auto_key,
        "bulletin_auto_kind": candidate.template_key,
        "bulletin_employee_user_id": candidate.profile.user_id,
    }
    post = Post.objects.create(
        author=author,
        title=candidate.title,
        body=candidate.body,
        kind=Post.PostType.ANNOUNCEMENT,
        module=Post.Module.BULLETIN,
        topic="hr",
        metadata=metadata,
        visibility=Post.Visibility.COMPANY,
        allow_comments=True,
        moderation_status=Post.ModerationStatus.PUBLISHED,
        published_at=timezone.now(),
    )
    record_audit_event(
        action="post.auto_celebration.created",
        actor=author,
        target=post,
        summary=f"Created automatic celebration post '{post.title}'",
        metadata={
            "template_file": template_path.name,
            "celebration_key": candidate.auto_key,
            "employee_user_id": candidate.profile.user_id,
        },
    )
    record_analytics_event(
        "feed",
        "auto_celebration_post_created",
        actor=author,
        metadata={
            "post_id": post.id,
            "template_key": candidate.template_key,
            "employee_user_id": candidate.profile.user_id,
        },
    )
    return post


def publish_celebration_post_from_preview(*, kind: str, user_id: int, template_name: str, reference_date: date | None = None) -> Post:
    reference_date = reference_date or timezone.localdate()
    author = _pick_company_author()
    profile = DirectoryProfile.objects.select_related("user").get(user_id=user_id)
    candidate = _build_candidate(kind, profile=profile, reference_date=reference_date)
    if _existing_auto_post(candidate.auto_key):
        raise RuntimeError("This celebration post has already been published for today.")
    template_kind = "birthday" if kind == "birthday" else "anniversary"
    template_path = TEMPLATE_ROOT / template_kind / template_name
    if not template_path.exists():
        raise RuntimeError("Selected template file was not found.")
    candidate_post = candidate
    card = _build_celebration_card(candidate_post, template_path=template_path)
    metadata = {
        "post_as_company": True,
        "company_author_name": "Acuité Ratings & Research",
        "company_author_title": "Official company post",
        "company_author_initials": "AR",
        "bulletin_category": "hr",
        "bulletin_template": candidate_post.template_key,
        "bulletin_meta_lines": candidate_post.meta_lines,
        "bulletin_card": card,
        "bulletin_template_file": template_path.name,
        "bulletin_auto_key": candidate_post.auto_key,
        "bulletin_auto_kind": candidate_post.template_key,
        "bulletin_employee_user_id": candidate_post.profile.user_id,
    }
    post = Post.objects.create(
        author=author,
        title=candidate_post.title,
        body=candidate_post.body,
        kind=Post.PostType.ANNOUNCEMENT,
        module=Post.Module.BULLETIN,
        topic="hr",
        metadata=metadata,
        visibility=Post.Visibility.COMPANY,
        allow_comments=True,
        moderation_status=Post.ModerationStatus.PUBLISHED,
        published_at=timezone.now(),
    )
    record_audit_event(
        action="post.admin_celebration.created",
        actor=author,
        target=post,
        summary=f"Created reviewed celebration post '{post.title}'",
        metadata={
            "template_file": template_path.name,
            "celebration_key": candidate_post.auto_key,
            "employee_user_id": candidate_post.profile.user_id,
        },
    )
    record_analytics_event(
        "feed",
        "admin_celebration_post_created",
        actor=author,
        metadata={
            "post_id": post.id,
            "template_key": candidate_post.template_key,
            "employee_user_id": candidate_post.profile.user_id,
        },
    )
    return post


def publish_daily_celebration_posts(*, reference_date: date | None = None, dry_run: bool = False) -> dict:
    reference_date = reference_date or timezone.localdate()
    author = _pick_company_author()
    created_posts = []
    skipped_keys = []

    candidates = []
    for profile in _active_profiles_for_date(reference_date, kind="birthday"):
        candidates.append(_build_birthday_candidate(profile, reference_date=reference_date))
    for profile in _active_profiles_for_date(reference_date, kind="anniversary"):
        candidates.append(_build_anniversary_candidate(profile, reference_date=reference_date))

    candidates.sort(key=lambda item: (item.profile.user.full_name.casefold(), item.template_key))

    for candidate in candidates:
        if _existing_auto_post(candidate.auto_key):
            skipped_keys.append(candidate.auto_key)
            continue
        if dry_run:
            created_posts.append(
                {
                    "title": candidate.title,
                    "template_key": candidate.template_key,
                    "employee_email": candidate.profile.user.email,
                    "auto_key": candidate.auto_key,
                }
            )
            continue
        post = _create_post_for_candidate(candidate, author=author)
        created_posts.append(
            {
                "post_id": post.id,
                "title": post.title,
                "template_key": candidate.template_key,
                "employee_email": candidate.profile.user.email,
                "auto_key": candidate.auto_key,
            }
        )

    return {
        "reference_date": reference_date.isoformat(),
        "created": created_posts,
        "skipped_existing": skipped_keys,
    }
