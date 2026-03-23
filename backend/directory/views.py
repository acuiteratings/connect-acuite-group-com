from django.db.models import Q
from django.http import JsonResponse

from .models import DirectoryProfile
from .serializers import serialize_directory_profile


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
        queryset = queryset.filter(user__department__iexact=department.strip())
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
            | Q(company_name__icontains=needle)
            | Q(function_name__icontains=needle)
            | Q(expertise__icontains=needle)
            | Q(bio__icontains=needle)
        )

    results = [serialize_directory_profile(profile) for profile in queryset.order_by("user__display_name", "user__email")[:500]]
    filters = {
        "company": sorted(
            value
            for value in base_queryset.values_list("company_name", flat=True).distinct()
            if value
        ),
        "department": sorted(
            value
            for value in base_queryset.values_list("user__department", flat=True).distinct()
            if value
        ),
        "function": sorted(
            value
            for value in base_queryset.values_list("function_name", flat=True).distinct()
            if value
        ),
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

# Create your views here.
