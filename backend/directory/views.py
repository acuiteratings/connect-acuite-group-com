import json

from django.db.models import Q
from django.http import HttpResponseNotAllowed, JsonResponse

from accounts.serializers import serialize_user
from store.services import build_coin_balance_map

from .community_utils import (
    COMMUNITY_CLUB_KEYS,
    COMMUNITY_CLUB_LIBRARY,
    community_hobby_labels_to_keys,
    normalize_community_clubs,
    normalize_community_hobby_labels,
)
from .models import CommunityMembership, DirectoryProfile
from .serializers import serialize_directory_profile
from .utils import (
    CONNECT_DEPARTMENT_LABELS,
    PROFILE_SKILL_LIBRARY,
    map_department_for_connect,
    normalize_profile_photos,
    resolve_branch_location,
    normalize_string_list,
)

DIRECTORY_DEFAULT_PAGE_SIZE = 500
DIRECTORY_MAX_PAGE_SIZE = 500


def _parse_json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return {}


def _distinct_values(queryset, field_name):
    return sorted(
        value
        for value in queryset.order_by().values_list(field_name, flat=True).distinct()
        if value
    )


def _profile_branch_location(profile):
    return resolve_branch_location(
        profile.office_location,
        profile.city,
        profile.user.location,
    )


def _collect_branch_locations(profiles):
    return sorted(
        {
            branch_location
            for profile in profiles
            for branch_location in [_profile_branch_location(profile)]
            if branch_location
        }
    )


def _positive_int(value, *, default, minimum=1, maximum=None):
    try:
        parsed = int(str(value or "").strip())
    except (TypeError, ValueError):
        parsed = default
    parsed = max(minimum, parsed)
    if maximum is not None:
        parsed = min(parsed, maximum)
    return parsed


def _pagination_payload(*, page, page_size, total_count):
    total_pages = max(1, (total_count + page_size - 1) // page_size)
    has_next = page < total_pages
    has_previous = page > 1
    return {
        "page": page,
        "page_size": page_size,
        "total_count": total_count,
        "total_pages": total_pages,
        "has_next": has_next,
        "has_previous": has_previous,
        "next_page": page + 1 if has_next else None,
        "previous_page": page - 1 if has_previous else None,
    }


def _get_or_create_profile_for_user(user):
    profile, _ = DirectoryProfile.objects.get_or_create(
        user=user,
        defaults={
            "city": user.location,
            "office_location": user.location,
            "department_for_connect": map_department_for_connect(user.department),
            "is_visible": True,
        },
    )
    return profile


def _sync_profile_clubs_for_user(user):
    if not user or not getattr(user, "pk", None):
        return []

    profile = _get_or_create_profile_for_user(user)
    desired_clubs = community_hobby_labels_to_keys(profile.hobbies)
    existing_memberships = {
        membership.club_key: membership
        for membership in CommunityMembership.objects.filter(user=user)
    }
    existing_clubs = set(existing_memberships.keys())
    desired_club_set = set(desired_clubs)
    affected_clubs = existing_clubs | desired_club_set

    for club_key in existing_clubs - desired_club_set:
        existing_memberships[club_key].delete()

    for club_key in desired_clubs:
        if club_key in existing_memberships:
            continue
        CommunityMembership.objects.create(
            user=user,
            club_key=club_key,
            is_admin=False,
        )

    for club_key in affected_clubs:
        if club_key in COMMUNITY_CLUB_KEYS:
            _ensure_club_admin(club_key)

    normalized_clubs = normalize_community_clubs(desired_clubs)
    if normalize_community_clubs(profile.clubs) != normalized_clubs:
        profile.clubs = normalized_clubs
        profile.save(update_fields=["clubs", "updated_at"])
    return normalized_clubs


def _ensure_club_admin(club_key):
    memberships = list(
        CommunityMembership.objects.filter(club_key=club_key)
        .order_by("joined_at", "id")
    )
    for index, membership in enumerate(memberships):
        should_be_admin = index == 0
        if membership.is_admin != should_be_admin:
            membership.is_admin = should_be_admin
            membership.save(update_fields=["is_admin", "updated_at"])


def _serialize_club_admin(user):
    if not user:
        return None
    payload = serialize_user(user)
    return {
        "id": payload["id"],
        "name": payload["name"],
        "title": payload["title"],
        "location": payload["location"],
        "initials": payload["initials"],
    }


def _build_communities_payload(current_user=None):
    if current_user and getattr(current_user, "is_authenticated", False):
        _sync_profile_clubs_for_user(current_user)

    memberships = list(
        CommunityMembership.objects.select_related("user")
        .filter(user__is_active=True)
        .order_by("club_key", "joined_at", "id")
    )
    member_counts = {item["key"]: 0 for item in COMMUNITY_CLUB_LIBRARY}
    club_admins = {}
    for membership in memberships:
        member_counts[membership.club_key] = member_counts.get(membership.club_key, 0) + 1
        if membership.club_key not in club_admins or membership.is_admin:
            club_admins[membership.club_key] = membership.user

    current_user_memberships = {}
    current_user_clubs = []
    if current_user and getattr(current_user, "is_authenticated", False):
        memberships = list(
            CommunityMembership.objects.filter(user=current_user)
            .order_by("joined_at", "id")
            .values("club_key", "is_admin")
        )
        current_user_memberships = {item["club_key"]: item for item in memberships}
        current_user_clubs = [item["club_key"] for item in memberships]

    results = [
        {
            **club,
            "member_count": member_counts.get(club["key"], 0),
            "joined": club["key"] in current_user_clubs,
            "viewer_is_admin": bool(current_user_memberships.get(club["key"], {}).get("is_admin")),
            "club_admin": _serialize_club_admin(club_admins.get(club["key"])),
        }
        for club in COMMUNITY_CLUB_LIBRARY
    ]
    return {
        "count": len(results),
        "joined_count": len(current_user_clubs),
        "my_clubs": current_user_clubs,
        "results": results,
    }


def directory_list(request):
    base_queryset = DirectoryProfile.objects.select_related("user", "manager").filter(
        user__is_active=True,
        is_visible=True,
        user__is_directory_visible=True,
    )
    queryset = base_queryset

    company = request.GET.get("company")
    department = request.GET.get("department")
    function_name = request.GET.get("function")
    location = resolve_branch_location(request.GET.get("location"))
    query = request.GET.get("q")

    if company:
        queryset = queryset.filter(company_name__iexact=company.strip())
    if department:
        queryset = queryset.filter(department_for_connect__iexact=department.strip())
    if function_name:
        queryset = queryset.filter(function_name__iexact=function_name.strip())
    if query:
        needle = query.strip()
        queryset = queryset.filter(
            Q(user__first_name__icontains=needle)
            | Q(user__last_name__icontains=needle)
            | Q(user__display_name__icontains=needle)
            | Q(user__email__icontains=needle)
            | Q(user__title__icontains=needle)
            | Q(user__department__icontains=needle)
            | Q(department_for_connect__icontains=needle)
            | Q(company_name__icontains=needle)
            | Q(function_name__icontains=needle)
            | Q(expertise__icontains=needle)
            | Q(bio__icontains=needle)
        )

    page = _positive_int(request.GET.get("page"), default=1)
    page_size = _positive_int(
        request.GET.get("page_size"),
        default=DIRECTORY_DEFAULT_PAGE_SIZE,
        maximum=DIRECTORY_MAX_PAGE_SIZE,
    )
    start = (page - 1) * page_size
    end = start + page_size
    ordered_queryset = queryset.order_by("user__display_name", "user__email")

    if location:
        profiles = list(ordered_queryset)
        matching_profiles = [
            profile for profile in profiles
            if _profile_branch_location(profile).casefold() == location.casefold()
        ]
        total_count = len(matching_profiles)
        profiles = matching_profiles[start:end]
    else:
        total_count = ordered_queryset.count()
        profiles = list(ordered_queryset[start:end])

    coin_balance_map = build_coin_balance_map(
        [profile.user_id for profile in profiles],
        refresh_expiry=False,
    )
    results = [
        serialize_directory_profile(profile, coin_balance=coin_balance_map.get(profile.user_id))
        for profile in profiles
    ]
    base_profiles = list(base_queryset.order_by("user__display_name", "user__email"))
    filters = {
        "company": _distinct_values(base_queryset, "company_name"),
        "department": [
            value
            for value in CONNECT_DEPARTMENT_LABELS
            if base_queryset.filter(department_for_connect=value).exists()
        ],
        "function": _distinct_values(base_queryset, "function_name"),
        "location": _collect_branch_locations(base_profiles),
    }
    return JsonResponse(
        {
            "count": total_count,
            "page_count": len(results),
            "results": results,
            "filters": filters,
            "pagination": _pagination_payload(
                page=page,
                page_size=page_size,
                total_count=total_count,
            ),
        }
    )


def communities_overview(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)

    if request.method == "GET":
        return JsonResponse(_build_communities_payload(request.user))

    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])
    return JsonResponse(
        {"detail": "Community membership is managed from My Profile hobbies."},
        status=400,
    )


def my_profile(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)

    profile = _get_or_create_profile_for_user(request.user)

    if request.method == "GET":
        return JsonResponse(
            {
                "profile": serialize_directory_profile(
                    profile,
                    include_profile_photos=True,
                    include_private_fields=True,
                ),
                "skill_library": PROFILE_SKILL_LIBRARY,
                "limits": {"max_photos": 2, "max_skills": 3, "max_hobbies": 3},
            }
        )

    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    payload = _parse_json_body(request)
    selected_skills = [
        skill
        for skill in normalize_string_list(payload.get("skills"), max_items=3)
        if skill in PROFILE_SKILL_LIBRARY
    ]
    profile.skills = selected_skills
    profile.hobbies = normalize_community_hobby_labels(payload.get("hobbies"), max_items=3)
    profile.interests = normalize_string_list(payload.get("interests"), max_items=12)
    profile.profile_photos = normalize_profile_photos(payload.get("profile_photos"), max_items=2)
    profile.save(update_fields=["skills", "hobbies", "interests", "profile_photos", "department_for_connect", "updated_at"])
    _sync_profile_clubs_for_user(request.user)
    profile.refresh_from_db()

    return JsonResponse(
        {
            "detail": "Profile updated successfully.",
            "profile": serialize_directory_profile(
                profile,
                include_profile_photos=True,
                include_private_fields=True,
            ),
            "skill_library": PROFILE_SKILL_LIBRARY,
            "limits": {"max_photos": 2, "max_skills": 3, "max_hobbies": 3},
        }
    )
