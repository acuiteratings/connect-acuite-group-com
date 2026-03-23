from django.http import JsonResponse

from .serializers import serialize_user


def current_user(request):
    if request.user.is_authenticated:
        permissions = sorted(request.user.get_all_permissions())
        return JsonResponse(
            {
                "authenticated": True,
                "user": serialize_user(request.user),
                "permissions": permissions,
            }
        )

    return JsonResponse(
        {
            "authenticated": False,
            "user": None,
            "permissions": [],
            "next_auth_decision": [
                "SSO",
                "email_otp",
                "google_or_microsoft_workspace",
            ],
        }
    )

# Create your views here.
