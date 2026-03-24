from django.http import HttpResponseNotAllowed, JsonResponse

from .services import build_recognition_overview


def recognition_overview(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    return JsonResponse(build_recognition_overview(request.user))
