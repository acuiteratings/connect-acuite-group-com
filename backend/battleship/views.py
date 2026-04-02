import json

from django.http import HttpResponseNotAllowed, JsonResponse

from accounts.models import User

from .models import BattleshipMatch
from .serializers import (
    serialize_candidate,
    serialize_match_brief,
    serialize_match_for_viewer,
)
from .services import (
    BattleshipRuleError,
    cancel_invitation,
    create_invitation,
    expire_stale_invitations,
    fire_turn,
    get_active_slot_match,
    get_candidate_users,
    get_match_queryset,
    get_open_match_for_user,
    office_policy_payload,
    request_rematch,
    resign_match,
    respond_to_invitation,
    submit_fleet_layout,
    sync_relevant_matches_for_user,
)


def _parse_json_body(request):
    if not request.body:
        return {}
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise BattleshipRuleError(
            "Request body must be valid JSON.",
            status=400,
            code="invalid_json",
        ) from exc


def _error_response(exc):
    payload = {"detail": exc.message, "code": exc.code}
    payload.update(exc.extra)
    return JsonResponse(payload, status=exc.status)


def _missing_match_response():
    return JsonResponse({"detail": "Battleship match not found."}, status=404)


def _employee_required(request):
    if not request.user.is_authenticated:
        return JsonResponse({"detail": "Authentication required."}, status=403)
    if not getattr(request.user, "has_employee_access", False):
        return JsonResponse(
            {"detail": "Only active employees can use Battleship."},
            status=403,
        )
    return None


def lobby(request):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    expire_stale_invitations(request=request)
    sync_relevant_matches_for_user(request.user, request=request)
    open_match = get_open_match_for_user(request.user)
    global_active_match = get_active_slot_match()
    query = request.GET.get("q", "").strip()
    incoming = list(
        get_match_queryset().filter(
            invitee=request.user,
            status="invited",
        )[:5]
    )
    outgoing = list(
        get_match_queryset().filter(
            inviter=request.user,
            status="invited",
        )[:5]
    )
    recent = list(
        get_match_queryset().filter(participants__user=request.user).exclude(
            status__in={"invited"}
        )[:8]
    )
    viewer_focus_match = open_match or (recent[0] if recent else None)
    candidates = get_candidate_users(viewer=request.user, query=query)
    return JsonResponse(
        {
            "office_policy": office_policy_payload(),
            "global_active_match": (
                serialize_match_brief(global_active_match, viewer=request.user)
                if global_active_match
                else None
            ),
            "viewer_open_match": (
                serialize_match_for_viewer(open_match, request.user) if open_match else None
            ),
            "viewer_match": (
                serialize_match_for_viewer(viewer_focus_match, request.user)
                if viewer_focus_match
                else None
            ),
            "incoming_invites": [
                serialize_match_brief(match, viewer=request.user) for match in incoming
            ],
            "outgoing_invites": [
                serialize_match_brief(match, viewer=request.user) for match in outgoing
            ],
            "recent_matches": [
                serialize_match_brief(match, viewer=request.user) for match in recent
            ],
            "candidate_people": [serialize_candidate(user) for user in candidates],
        }
    )


def candidates(request):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    query = request.GET.get("q", "").strip()
    users = get_candidate_users(viewer=request.user, query=query)
    return JsonResponse({"count": len(users), "results": [serialize_candidate(user) for user in users]})


def invite_collection(request):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        payload = _parse_json_body(request)
        invitee_id = payload.get("invitee_user_id")
        if not invitee_id:
            raise BattleshipRuleError("invitee_user_id is required.", status=400, code="missing_invitee")
        try:
            invitee_id = int(invitee_id)
        except (TypeError, ValueError) as exc:
            raise BattleshipRuleError("invitee_user_id must be a valid user ID.", status=400, code="invalid_invitee") from exc
        try:
            invitee = User.objects.get(
                pk=invitee_id,
                is_active=True,
                employment_status=User.EmploymentStatus.ACTIVE,
                access_level__in={
                    User.AccessLevel.EMPLOYEE,
                    User.AccessLevel.MANAGER,
                    User.AccessLevel.MODERATOR,
                    User.AccessLevel.ADMIN,
                },
            )
        except User.DoesNotExist as exc:
            raise BattleshipRuleError(
                "The selected employee could not be found.",
                status=404,
                code="invitee_missing",
            ) from exc
        match = create_invitation(request.user, invitee, request=request)
    except BattleshipRuleError as exc:
        return _error_response(exc)
    return JsonResponse({"match": serialize_match_for_viewer(match, request.user)}, status=201)


def match_state(request, match_id):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])
    try:
        from .services import load_match_for_viewer

        match = load_match_for_viewer(match_id, request.user, request=request)
    except BattleshipMatch.DoesNotExist:
        return _missing_match_response()
    except BattleshipRuleError as exc:
        return _error_response(exc)
    return JsonResponse({"match": serialize_match_for_viewer(match, request.user)})


def match_respond(request, match_id):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        payload = _parse_json_body(request)
        match = respond_to_invitation(
            match_id,
            request.user,
            payload.get("decision"),
            request=request,
        )
    except BattleshipMatch.DoesNotExist:
        return _missing_match_response()
    except BattleshipRuleError as exc:
        return _error_response(exc)
    return JsonResponse({"match": serialize_match_for_viewer(match, request.user)})


def match_cancel(request, match_id):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        cancel_invitation(match_id, request.user, request=request)
    except BattleshipMatch.DoesNotExist:
        return _missing_match_response()
    except BattleshipRuleError as exc:
        return _error_response(exc)
    return JsonResponse({"ok": True, "detail": "Invitation cancelled."})


def match_placement(request, match_id):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        payload = _parse_json_body(request)
        match = submit_fleet_layout(
            match_id,
            request.user,
            payload.get("fleet_layout"),
            request=request,
        )
    except BattleshipMatch.DoesNotExist:
        return _missing_match_response()
    except BattleshipRuleError as exc:
        return _error_response(exc)
    return JsonResponse({"match": serialize_match_for_viewer(match, request.user)})


def match_fire(request, match_id):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        payload = _parse_json_body(request)
        match = fire_turn(
            match_id,
            request.user,
            payload.get("row"),
            payload.get("col"),
            request=request,
        )
    except BattleshipMatch.DoesNotExist:
        return _missing_match_response()
    except BattleshipRuleError as exc:
        return _error_response(exc)
    return JsonResponse({"match": serialize_match_for_viewer(match, request.user)})


def match_resign(request, match_id):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        match = resign_match(match_id, request.user, request=request)
    except BattleshipMatch.DoesNotExist:
        return _missing_match_response()
    except BattleshipRuleError as exc:
        return _error_response(exc)
    return JsonResponse({"match": serialize_match_for_viewer(match, request.user)})


def match_rematch(request, match_id):
    forbidden = _employee_required(request)
    if forbidden:
        return forbidden
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    try:
        match = request_rematch(match_id, request.user, request=request)
    except BattleshipMatch.DoesNotExist:
        return _missing_match_response()
    except BattleshipRuleError as exc:
        return _error_response(exc)
    return JsonResponse({"match": serialize_match_for_viewer(match, request.user)}, status=201)
