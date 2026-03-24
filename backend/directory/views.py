import json

from django.db.models import Q
from django.http import HttpResponseNotAllowed, JsonResponse

from .models import DirectoryProfile
from .serializers import serialize_directory_profile
from .utils import (
    CONNECT_DEPARTMENT_LABELS,
    PROFILE_SKILL_LIBRARY,
    map_department_for_connect,
    normalize_profile_photos,
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
    location = request.GET.get("location")
    query = request.GET.get("q")

    if company:
        queryset = queryset.filter(company_name__iexact=company.strip())
    if department:
        queryset = queryset.filter(department_for_connect__iexact=department.strip())
    if function_name:
        queryset = queryset.filter(function_name__iexact=function_name.strip())
    if location:
        queryset = queryset.filter(
            Q(city__iexact=location.strip())
            | Q(office_location__iexact=location.strip())
            | Q(user__location__iexact=location.strip())
        )
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

    results = [serialize_directory_profile(profile) for profile in queryset.order_by("user__display_name", "user__email")[:500]]
    filters = {
        "company": _distinct_values(base_queryset, "company_name"),
        "department": [
            value
            for value in CONNECT_DEPARTMENT_LABELS
            if base_queryset.filter(department_for_connect=value).exists()
        ],
        "function": _distinct_values(base_queryset, "function_name"),
        "location": sorted(
            {
                value
                for value in list(base_queryset.values_list("city", flat=True))
                + list(base_queryset.values_list("office_location", flat=True))
                + list(base_queryset.values_list("user__location", flat=True))
                if value
            }
        ),
    }
    return JsonResponse({"count": len(results), "results": results, "filters": filters})


def my_profile(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)

    profile, _ = DirectoryProfile.objects.get_or_create(
        user=request.user,
        defaults={
            "city": request.user.location,
            "office_location": request.user.location,
            "department_for_connect": map_department_for_connect(request.user.department),
            "is_visible": True,
        },
    )

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
    profile.skills = selected_skills
    profile.hobbies = normalize_string_list(payload.get("hobbies"), max_items=12)
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
