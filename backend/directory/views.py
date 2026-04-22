import json

from django.db.models import Q
from django.http import HttpResponseNotAllowed, JsonResponse

from store.services import build_coin_balance_map

from .community_utils import COMMUNITY_CLUB_LIBRARY, normalize_community_clubs
from .models import DirectoryProfile
from .serializers import serialize_directory_profile
from .utils import (
    CONNECT_DEPARTMENT_LABELS,
    PROFILE_SKILL_LIBRARY,
    map_department_for_connect,
    normalize_profile_photos,
    resolve_branch_location,
    normalize_string_list,
)


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


def _build_communities_payload(current_user=None):
    profiles = list(
        DirectoryProfile.objects.select_related("user").filter(user__is_active=True)
    )
    member_counts = {item["key"]: 0 for item in COMMUNITY_CLUB_LIBRARY}
    for profile in profiles:
        for club_key in normalize_community_clubs(profile.clubs):
            member_counts[club_key] += 1

    current_user_clubs = []
    if current_user and getattr(current_user, "is_authenticated", False):
        profile = _get_or_create_profile_for_user(current_user)
        current_user_clubs = normalize_community_clubs(profile.clubs)

    results = [
        {
            **club,
            "member_count": member_counts.get(club["key"], 0),
            "joined": club["key"] in current_user_clubs,
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

    profiles = list(queryset.order_by("user__display_name", "user__email"))
    if location:
        profiles = [
            profile for profile in profiles
            if _profile_branch_location(profile).casefold() == location.casefold()
        ]
    profiles = profiles[:500]
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
    return JsonResponse({"count": len(results), "results": results, "filters": filters})


def communities_overview(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)

    if request.method == "GET":
        return JsonResponse(_build_communities_payload(request.user))

    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    payload = _parse_json_body(request)
    club_key = str(payload.get("club_key", "")).strip().lower()
    action = str(payload.get("action", "")).strip().lower()
    if club_key not in {item["key"] for item in COMMUNITY_CLUB_LIBRARY}:
        return JsonResponse({"detail": "Invalid community selected."}, status=400)
    if action not in {"join", "leave"}:
        return JsonResponse({"detail": "Invalid membership action."}, status=400)

    profile = _get_or_create_profile_for_user(request.user)
    clubs = normalize_community_clubs(profile.clubs)
    if action == "join" and club_key not in clubs:
        clubs.append(club_key)
    if action == "leave":
        clubs = [item for item in clubs if item != club_key]
    profile.clubs = clubs
    profile.save(update_fields=["clubs", "updated_at"])

    return JsonResponse(_build_communities_payload(request.user))


def my_profile(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)

    profile = _get_or_create_profile_for_user(request.user)

    if request.method == "GET":
        return JsonResponse(
            {
                "profile": serialize_directory_profile(profile),
                "skill_library": PROFILE_SKILL_LIBRARY,
                "limits": {"max_photos": 2, "max_skills": 10},
            }
        )

    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    payload = _parse_json_body(request)
    selected_skills = [
        skill
        for skill in normalize_string_list(payload.get("skills"), max_items=10)
        if skill in PROFILE_SKILL_LIBRARY
    ]
    allowed_hobby_labels = {item["label"] for item in COMMUNITY_CLUB_LIBRARY}
    profile.skills = selected_skills
    profile.hobbies = [
        hobby
        for hobby in normalize_string_list(payload.get("hobbies"), max_items=12)
        if hobby in allowed_hobby_labels
    ]
    profile.interests = normalize_string_list(payload.get("interests"), max_items=12)
    profile.profile_photos = normalize_profile_photos(payload.get("profile_photos"), max_items=2)
    profile.save(update_fields=["skills", "hobbies", "interests", "profile_photos", "department_for_connect", "updated_at"])

    return JsonResponse(
        {
            "detail": "Profile updated successfully.",
            "profile": serialize_directory_profile(profile),
            "skill_library": PROFILE_SKILL_LIBRARY,
            "limits": {"max_photos": 2, "max_skills": 10},
        }
    )
