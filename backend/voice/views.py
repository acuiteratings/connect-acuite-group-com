import json

from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone

from operations.services import record_analytics_event, record_audit_event

from .models import Poll, PollOption, PollVote
from .serializers import serialize_poll


def _parse_json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError("Request body must be valid JSON.") from exc


def active_poll(request):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    poll = Poll.objects.filter(is_active=True).order_by("-created_at").first()
    return JsonResponse({"poll": serialize_poll(poll, voter=request.user) if poll else None})


def vote_on_poll(request, poll_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)

    poll = get_object_or_404(Poll, pk=poll_id, is_active=True)
    if not poll.is_open:
        return JsonResponse({"detail": "This poll is no longer open."}, status=400)

    try:
        payload = _parse_json_body(request)
    except ValueError as exc:
        return JsonResponse({"detail": str(exc)}, status=400)

    option_id = payload.get("option_id")
    if not option_id:
        return JsonResponse({"detail": "option_id is required."}, status=400)

    option = get_object_or_404(PollOption, pk=option_id, poll=poll)
    vote, created = PollVote.objects.update_or_create(
        poll=poll,
        voter=request.user,
        defaults={"option": option},
    )
    action_name = "voice.poll_vote_created" if created else "voice.poll_vote_updated"
    record_audit_event(
        action=action_name,
        actor=request.user,
        target=vote,
        summary=f"Voted on poll '{poll.question}'",
        metadata={"poll_id": poll.id, "option_id": option.id},
        request=request,
    )
    record_analytics_event(
        "voice",
        "poll_voted",
        actor=request.user,
        metadata={"poll_id": poll.id, "option_id": option.id},
        request=request,
    )
    poll.updated_at = timezone.now()
    poll.save(update_fields=["updated_at"])
    return JsonResponse({"poll": serialize_poll(poll, voter=request.user)})
