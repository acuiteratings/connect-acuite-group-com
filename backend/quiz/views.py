import json

from django.http import HttpResponseNotAllowed, JsonResponse

from accounts.models import User

from .serializers import serialize_candidate, serialize_match_brief, serialize_match_state
from .services import (
    QuizRuleError,
    advance_match_if_needed,
    answer_question,
    cancel_match,
    create_match,
    get_candidate_users,
    get_match_queryset,
    load_match_for_user,
    respond_to_invitation,
    start_match,
)


def _parse_json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise QuizRuleError("Request body must be valid JSON.", status=400, code="invalid_json") from exc


def _error_response(exc):
    return JsonResponse({"detail": exc.message, "code": exc.code}, status=exc.status)


def _employee_required(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)
    if not getattr(request.user, "has_employee_access", False):
        return JsonResponse({"detail": "Only active employees can use Playtime quiz."}, status=403)
    return None


def lobby(request):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    query = request.GET.get("q", "").strip()
    matches = get_match_queryset().filter(participants__user=request.user).distinct()
    open_matches = matches.filter(status__in={"invited", "active"})[:10]
    incoming = []
    outgoing = []
    active_match = None
    for match in open_matches:
        participant = match.participants.filter(user=request.user).first()
        if match.status == "active" and active_match is None:
            active_match = match
        elif participant and participant.status == "invited":
            incoming.append(match)
        elif match.host_id == request.user.id:
            outgoing.append(match)
    recent = matches.filter(status__in={"completed", "cancelled"})[:8]
    candidates_list = get_candidate_users(request.user, query=query)
    return JsonResponse(
        {
            "viewer_active_match": serialize_match_brief(active_match, viewer=request.user) if active_match else None,
            "incoming_invites": [serialize_match_brief(match, viewer=request.user) for match in incoming],
            "outgoing_invites": [serialize_match_brief(match, viewer=request.user) for match in outgoing],
            "recent_matches": [serialize_match_brief(match, viewer=request.user) for match in recent],
            "candidate_people": [serialize_candidate(user) for user in candidates_list],
        }
    )


def candidates(request):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    users = get_candidate_users(request.user, query=request.GET.get("q", ""))
    return JsonResponse({"count": len(users), "results": [serialize_candidate(user) for user in users]})


def matches_collection(request):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        payload = _parse_json_body(request)
        match = create_match(
            request.user,
            payload.get("invitee_user_ids") or [],
            payload.get("difficulty"),
            request=request,
        )
    except QuizRuleError as exc:
        return _error_response(exc)
    return JsonResponse({"match": serialize_match_state(match, request.user)}, status=201)


def match_state(request, match_id):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    try:
        match = load_match_for_user(match_id, request.user)
        match = advance_match_if_needed(match.id)
        match = load_match_for_user(match.id, request.user)
    except QuizRuleError as exc:
        return _error_response(exc)
    except Exception:
        return JsonResponse({"detail": "Quiz match not found."}, status=404)
    return JsonResponse({"match": serialize_match_state(match, request.user)})


def match_respond(request, match_id):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        payload = _parse_json_body(request)
        match = respond_to_invitation(match_id, request.user, payload.get("decision"), request=request)
        match = load_match_for_user(match.id, request.user)
    except QuizRuleError as exc:
        return _error_response(exc)
    except Exception:
        return JsonResponse({"detail": "Quiz match not found."}, status=404)
    return JsonResponse({"match": serialize_match_state(match, request.user)})


def match_start(request, match_id):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        match = start_match(match_id, request.user, request=request)
        match = load_match_for_user(match.id, request.user)
    except QuizRuleError as exc:
        return _error_response(exc)
    except Exception:
        return JsonResponse({"detail": "Quiz match not found."}, status=404)
    return JsonResponse({"match": serialize_match_state(match, request.user)})


def match_answer(request, match_id):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        payload = _parse_json_body(request)
        match = answer_question(match_id, request.user, payload.get("selected_option"), request=request)
        match = load_match_for_user(match.id, request.user)
    except QuizRuleError as exc:
        return _error_response(exc)
    except Exception:
        return JsonResponse({"detail": "Quiz match not found."}, status=404)
    return JsonResponse({"match": serialize_match_state(match, request.user)})


def match_cancel(request, match_id):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        match = cancel_match(match_id, request.user, request=request)
        match = load_match_for_user(match.id, request.user)
    except QuizRuleError as exc:
        return _error_response(exc)
    except Exception:
        return JsonResponse({"detail": "Quiz match not found."}, status=404)
    return JsonResponse({"match": serialize_match_state(match, request.user)})
