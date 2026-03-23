from django.db.models import Q
from django.http import JsonResponse

from .models import DirectoryProfile
from .serializers import serialize_directory_profile


def directory_list(request):
    queryset = DirectoryProfile.objects.select_related("user", "manager").filter(
        user__is_active=True,
        is_visible=True,
        user__is_directory_visible=True,
    )

    department = request.GET.get("department")
    location = request.GET.get("location")
    query = request.GET.get("q")

    if department:
        queryset = queryset.filter(user__department__icontains=department.strip())
    if location:
        queryset = queryset.filter(
            Q(city__icontains=location.strip())
            | Q(office_location__icontains=location.strip())
            | Q(user__location__icontains=location.strip())
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
            | Q(expertise__icontains=needle)
            | Q(bio__icontains=needle)
        )

    results = [serialize_directory_profile(profile) for profile in queryset[:100]]
    return JsonResponse({"count": len(results), "results": results})

# Create your views here.
