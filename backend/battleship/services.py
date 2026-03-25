import secrets
from dataclasses import dataclass
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from django.conf import settings
from django.db import IntegrityError, models, transaction
from django.utils import timezone

from accounts.models import User
from operations.services import record_audit_event

from .models import BattleshipEvent, BattleshipMatch, BattleshipParticipant, BattleshipShot

GRID_SIZE = 10
ROW_LABELS = "ABCDEFGHIJ"
SERIOUS_MATCH_STATUSES = {
    BattleshipMatch.Status.SHIP_PLACEMENT,
    BattleshipMatch.Status.ACTIVE,
    BattleshipMatch.Status.PAUSED_OFFICE_HOURS,
}
OPEN_MATCH_STATUSES = SERIOUS_MATCH_STATUSES | {
    BattleshipMatch.Status.INVITED,
}
FLEET_SPEC = (
    {"ship_type": "carrier", "label": "Carrier", "size": 5},
    {"ship_type": "battleship", "label": "Battleship", "size": 4},
    {"ship_type": "cruiser", "label": "Cruiser", "size": 3},
    {"ship_type": "submarine", "label": "Submarine", "size": 3},
    {"ship_type": "destroyer", "label": "Destroyer", "size": 2},
)
FLEET_BY_TYPE = {item["ship_type"]: item for item in FLEET_SPEC}
EMPLOYEE_ACCESS_LEVELS = {
    User.AccessLevel.EMPLOYEE,
    User.AccessLevel.MANAGER,
    User.AccessLevel.MODERATOR,
    User.AccessLevel.ADMIN,
}


class BattleshipRuleError(Exception):
    def __init__(self, message, *, status=400, code="battleship_rule_error", extra=None):
        super().__init__(message)
        self.message = message
        self.status = status
        self.code = code
        self.extra = extra or {}


@dataclass(frozen=True)
class OfficeWindow:
    start: time
    end: time

    def contains(self, value: time) -> bool:
        return self.start <= value < self.end


def get_now():
    return timezone.now()


def get_office_timezone():
    return ZoneInfo(getattr(settings, "BATTLESHIP_TIMEZONE", settings.TIME_ZONE))


def get_office_windows():
    windows = []
    raw_windows = getattr(
        settings,
        "BATTLESHIP_BLOCK_WINDOWS",
        [("10:00", "13:00"), ("14:00", "18:30")],
    )
    for start_value, end_value in raw_windows:
        start = time.fromisoformat(str(start_value))
        end = time.fromisoformat(str(end_value))
        windows.append(OfficeWindow(start=start, end=end))
    return sorted(windows, key=lambda item: item.start)


def office_now(now=None):
    return timezone.localtime(now or get_now(), get_office_timezone())


def coordinate_label(row, col):
    return f"{ROW_LABELS[row]}{col + 1}"


def get_current_block_window(now=None):
    local_now = office_now(now)
    current_time = local_now.timetz().replace(tzinfo=None)
    for window in get_office_windows():
        if window.contains(current_time):
            return window
    return None


def is_office_blocked(now=None):
    return get_current_block_window(now=now) is not None


def get_next_allowed_time(now=None):
    local_now = office_now(now)
    current_window = get_current_block_window(now=local_now)
    if current_window:
        return timezone.make_aware(
            datetime.combine(local_now.date(), current_window.end),
            get_office_timezone(),
        )
    return local_now


def get_inactivity_timeout():
    return timedelta(
        minutes=int(getattr(settings, "BATTLESHIP_INACTIVITY_TIMEOUT_MINUTES", 30))
    )


def get_invitation_ttl():
    return timedelta(
        minutes=int(getattr(settings, "BATTLESHIP_INVITE_TTL_MINUTES", 120))
    )


def get_poll_interval_seconds():
    return int(getattr(settings, "BATTLESHIP_POLL_INTERVAL_SECONDS", 4))


def office_policy_payload(now=None):
    local_now = office_now(now)
    blocked = is_office_blocked(now=local_now)
    next_allowed = get_next_allowed_time(now=local_now)
    current_window = get_current_block_window(now=local_now)
    return {
        "timezone": getattr(settings, "BATTLESHIP_TIMEZONE", settings.TIME_ZONE),
        "blocked": blocked,
        "current_time": local_now.isoformat(),
        "current_time_label": local_now.strftime("%d %b %Y, %I:%M %p"),
        "windows": [
            {
                "start": window.start.strftime("%H:%M"),
                "end": window.end.strftime("%H:%M"),
                "label": f"{window.start.strftime('%I:%M %p')} - {window.end.strftime('%I:%M %p')}",
            }
            for window in get_office_windows()
        ],
        "current_window_label": (
            f"{current_window.start.strftime('%I:%M %p')} - {current_window.end.strftime('%I:%M %p')}"
            if current_window
            else ""
        ),
        "next_allowed_at": next_allowed.isoformat() if next_allowed else None,
        "next_allowed_label": next_allowed.strftime("%d %b %Y, %I:%M %p") if next_allowed else "",
        "message": (
            "Game paused due to office peak hours."
            if blocked
            else "Battleship is currently available."
        ),
        "poll_interval_seconds": get_poll_interval_seconds(),
    }


def create_event(match, event_type, summary, *, actor=None, metadata=None, request=None):
    event = BattleshipEvent.objects.create(
        match=match,
        actor=actor if getattr(actor, "is_authenticated", False) else actor,
        event_type=event_type,
        summary=summary,
        metadata=metadata or {},
    )
    record_audit_event(
        action=f"battleship.{event_type}",
        summary=summary,
        actor=actor,
        target=match,
        metadata=metadata or {},
        request=request,
    )
    return event


def fleet_spec_payload():
    return [dict(item) for item in FLEET_SPEC]


def normalize_orientation(value):
    normalized = str(value or "").strip().lower()
    if normalized in {"h", "horizontal"}:
        return "horizontal"
    if normalized in {"v", "vertical"}:
        return "vertical"
    raise BattleshipRuleError(
        "Ships may be placed only horizontally or vertically.",
        code="invalid_orientation",
    )


def build_ship_cells(row, col, orientation, size):
    cells = []
    for offset in range(size):
        target_row = row + offset if orientation == "vertical" else row
        target_col = col + offset if orientation == "horizontal" else col
        if target_row < 0 or target_row >= GRID_SIZE or target_col < 0 or target_col >= GRID_SIZE:
            raise BattleshipRuleError(
                "Ships cannot go outside the 10x10 board.",
                code="ship_out_of_bounds",
            )
        cells.append(
            {
                "row": target_row,
                "col": target_col,
                "label": coordinate_label(target_row, target_col),
            }
        )
    return cells


def validate_fleet_layout(layout):
    if not isinstance(layout, list):
        raise BattleshipRuleError(
            "Fleet layout must be a list of ship placements.",
            code="invalid_layout",
        )
    if len(layout) != len(FLEET_SPEC):
        raise BattleshipRuleError(
            "All five ships must be placed before battle can begin.",
            code="fleet_incomplete",
        )

    normalized = []
    seen_ship_types = set()
    occupied_cells = {}
    for placement in layout:
        ship_type = str((placement or {}).get("ship_type") or "").strip().lower()
        ship_spec = FLEET_BY_TYPE.get(ship_type)
        if not ship_spec:
            raise BattleshipRuleError("An unknown ship type was submitted.", code="unknown_ship")
        if ship_type in seen_ship_types:
            raise BattleshipRuleError("Each ship may be placed only once.", code="duplicate_ship")

        try:
            row = int((placement or {}).get("row"))
            col = int((placement or {}).get("col"))
        except (TypeError, ValueError) as exc:
            raise BattleshipRuleError(
                "Ship coordinates must be valid board cells.",
                code="invalid_coordinates",
            ) from exc

        if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE:
            raise BattleshipRuleError(
                "Ship coordinates must stay within the board.",
                code="invalid_coordinates",
            )

        orientation = normalize_orientation((placement or {}).get("orientation"))
        cells = build_ship_cells(row, col, orientation, ship_spec["size"])

        for cell in cells:
            key = (cell["row"], cell["col"])
            if key in occupied_cells:
                raise BattleshipRuleError(
                    "Ships cannot overlap.",
                    code="ship_overlap",
                    extra={"cell": coordinate_label(*key)},
                )
            occupied_cells[key] = ship_type

        normalized.append(
            {
                "ship_type": ship_type,
                "label": ship_spec["label"],
                "size": ship_spec["size"],
                "row": row,
                "col": col,
                "orientation": orientation,
                "cells": cells,
            }
        )
        seen_ship_types.add(ship_type)

    return sorted(normalized, key=lambda item: item["size"], reverse=True)


def get_match_queryset():
    return BattleshipMatch.objects.select_related(
        "inviter",
        "invitee",
        "turn_owner",
        "winner",
        "loser",
        "resigned_by",
        "inactive_player",
    ).prefetch_related(
        "participants__user",
        "events__actor",
    )


def get_participant(match, user):
    for participant in match.participants.all():
        if participant.user_id == user.id:
            return participant
    raise BattleshipRuleError(
        "You are not part of this match.",
        status=403,
        code="forbidden_match_access",
    )


def get_opponent_participant(match, participant):
    for candidate in match.participants.all():
        if candidate.pk != participant.pk:
            return candidate
    raise BattleshipRuleError("Opponent data is unavailable.", code="opponent_missing")


def get_open_match_for_user(user):
    if not getattr(user, "is_authenticated", False):
        return None
    matches = list(
        get_match_queryset().filter(
            participants__user=user,
            status__in=OPEN_MATCH_STATUSES,
        )
    )
    if not matches:
        return None

    def _priority(item):
        if item.status in SERIOUS_MATCH_STATUSES:
            return 0
        if item.status == BattleshipMatch.Status.INVITED and item.invitee_id == user.id:
            return 1
        return 2

    return sorted(matches, key=lambda item: (_priority(item), -item.id))[0]


def expire_stale_invitations(*, request=None, now=None):
    current_time = now or get_now()
    stale_matches = list(
        BattleshipMatch.objects.filter(
            status=BattleshipMatch.Status.INVITED,
            invitation_expires_at__isnull=False,
            invitation_expires_at__lte=current_time,
        )
    )
    for match in stale_matches:
        match.status = BattleshipMatch.Status.EXPIRED
        match.responded_at = current_time
        match.save(update_fields=["status", "responded_at", "updated_at"])
        create_event(
            match,
            BattleshipEvent.EventType.INVITE_EXPIRED,
            "Invitation expired before it was accepted.",
            metadata={"match_id": match.id},
            request=request,
        )
    return stale_matches


def get_active_slot_match(exclude_match_id=None):
    queryset = get_match_queryset().filter(occupies_global_slot=True)
    if exclude_match_id:
        queryset = queryset.exclude(pk=exclude_match_id)
    return queryset.first()


def ensure_actions_allowed(match=None, *, now=None, request=None):
    if match is not None:
        sync_match_state(match, now=now, request=request)
    if is_office_blocked(now=now):
        raise BattleshipRuleError(
            "Battleship is paused during office peak hours.",
            status=409,
            code="office_hours_blocked",
            extra={"office_policy": office_policy_payload(now=now)},
        )


def get_inactive_deadline(match):
    if not match.last_activity_at:
        return None
    return match.last_activity_at + get_inactivity_timeout()


def identify_inactive_player(match):
    if match.status == BattleshipMatch.Status.ACTIVE:
        return match.turn_owner
    if match.status == BattleshipMatch.Status.SHIP_PLACEMENT:
        not_ready = [item for item in match.participants.all() if not item.placement_ready]
        if not_ready:
            return not_ready[0].user
    return None


def finalize_match_as_abandoned(match, *, now=None, request=None):
    current_time = now or get_now()
    inactive_player = identify_inactive_player(match)
    winner = None
    loser = inactive_player
    if inactive_player:
        for participant in match.participants.all():
            if participant.user_id != inactive_player.id:
                winner = participant.user
                break
    match.status = BattleshipMatch.Status.ABANDONED
    match.occupies_global_slot = False
    match.completed_at = current_time
    match.winner = winner
    match.loser = loser
    match.inactive_player = inactive_player
    match.turn_owner = None
    match.save(
        update_fields=[
            "status",
            "occupies_global_slot",
            "completed_at",
            "winner",
            "loser",
            "inactive_player",
            "turn_owner",
            "updated_at",
        ]
    )
    create_event(
        match,
        BattleshipEvent.EventType.MATCH_ABANDONED,
        "Match closed because one player became inactive.",
        actor=winner,
        metadata={"inactive_player_id": inactive_player.id if inactive_player else None},
        request=request,
    )


def sync_match_state(match, *, now=None, request=None):
    current_time = now or get_now()
    changed = False

    if (
        match.status == BattleshipMatch.Status.INVITED
        and match.invitation_expires_at
        and match.invitation_expires_at <= current_time
    ):
        match.status = BattleshipMatch.Status.EXPIRED
        match.responded_at = current_time
        match.save(update_fields=["status", "responded_at", "updated_at"])
        create_event(
            match,
            BattleshipEvent.EventType.INVITE_EXPIRED,
            "Invitation expired before it was accepted.",
            metadata={"match_id": match.id},
            request=request,
        )
        return match

    if (
        match.status in {
            BattleshipMatch.Status.SHIP_PLACEMENT,
            BattleshipMatch.Status.ACTIVE,
        }
        and is_office_blocked(now=current_time)
    ):
        match.paused_from_status = match.status
        match.status = BattleshipMatch.Status.PAUSED_OFFICE_HOURS
        match.last_activity_at = current_time
        match.save(update_fields=["paused_from_status", "status", "last_activity_at", "updated_at"])
        create_event(
            match,
            BattleshipEvent.EventType.MATCH_PAUSED,
            "Game paused due to office peak hours.",
            metadata={"paused_from_status": match.paused_from_status},
            request=request,
        )
        changed = True

    if match.status == BattleshipMatch.Status.PAUSED_OFFICE_HOURS and not is_office_blocked(now=current_time):
        resume_status = (
            match.paused_from_status
            if match.paused_from_status in {
                BattleshipMatch.Status.SHIP_PLACEMENT,
                BattleshipMatch.Status.ACTIVE,
            }
            else BattleshipMatch.Status.ACTIVE
        )
        match.status = resume_status
        match.paused_from_status = ""
        match.last_activity_at = current_time
        match.save(update_fields=["status", "paused_from_status", "last_activity_at", "updated_at"])
        create_event(
            match,
            BattleshipEvent.EventType.MATCH_RESUMED,
            "Game resumed after office peak hours.",
            metadata={"resumed_to": resume_status},
            request=request,
        )
        changed = True

    deadline = get_inactive_deadline(match)
    if (
        match.status in {
            BattleshipMatch.Status.SHIP_PLACEMENT,
            BattleshipMatch.Status.ACTIVE,
        }
        and deadline
        and current_time >= deadline
    ):
        finalize_match_as_abandoned(match, now=current_time, request=request)
        changed = True

    if changed:
        match.refresh_from_db()
    return match


def choose_first_turn(match):
    participants = list(match.participants.all())
    if len(participants) != 2:
        raise BattleshipRuleError(
            "A Battleship match requires exactly two players.",
            code="invalid_participant_count",
        )
    return participants[secrets.randbelow(2)].user


def layout_cell_map(layout):
    cells = {}
    for ship in layout or []:
        for cell in ship.get("cells", []):
            cells[(cell["row"], cell["col"])] = ship["ship_type"]
    return cells


def ship_cells_by_type(layout):
    return {
        ship["ship_type"]: {(cell["row"], cell["col"]) for cell in ship.get("cells", [])}
        for ship in layout or []
    }


def get_ship_hit_map(participant):
    shots = BattleshipShot.objects.filter(target_participant=participant)
    hit_map = {}
    for shot in shots.exclude(result=BattleshipShot.Result.MISS):
        hit_map.setdefault(shot.ship_type, set()).add((shot.row, shot.col))
    return hit_map


def resolve_shot(target_participant, row, col):
    layout = target_participant.fleet_layout or []
    cell_map = layout_cell_map(layout)
    ship_type = cell_map.get((row, col))
    if not ship_type:
        return {
            "result": BattleshipShot.Result.MISS,
            "ship_type": "",
            "all_sunk": False,
        }

    ship_map = ship_cells_by_type(layout)
    prior_hits = get_ship_hit_map(target_participant)
    current_hits = set(prior_hits.get(ship_type, set()))
    current_hits.add((row, col))
    result = (
        BattleshipShot.Result.SUNK
        if current_hits >= ship_map.get(ship_type, set())
        else BattleshipShot.Result.HIT
    )
    all_sunk = True
    for candidate_ship_type, cells in ship_map.items():
        hits = set(prior_hits.get(candidate_ship_type, set()))
        if candidate_ship_type == ship_type:
            hits = current_hits
        if hits < cells:
            all_sunk = False
            break

    return {
        "result": result,
        "ship_type": ship_type,
        "all_sunk": all_sunk,
    }


def format_move_summary(shot):
    coord = coordinate_label(shot.row, shot.col)
    result_label = {
        BattleshipShot.Result.HIT: "hit",
        BattleshipShot.Result.MISS: "miss",
        BattleshipShot.Result.SUNK: (
            f"sunk {FLEET_BY_TYPE.get(shot.ship_type, {}).get('label', shot.ship_type)}"
        ),
    }[shot.result]
    return f"{coord} {result_label}"


def claim_global_slot(match):
    match.occupies_global_slot = True
    try:
        match.save(update_fields=["occupies_global_slot", "updated_at"])
    except IntegrityError as exc:
        raise BattleshipRuleError(
            "Another Battleship match is already in progress across Connect.",
            status=409,
            code="global_slot_occupied",
        ) from exc


def create_invitation(inviter, invitee, *, request=None, rematch_parent=None, now=None):
    current_time = now or get_now()
    if inviter.id == invitee.id:
        raise BattleshipRuleError("You cannot invite yourself to Battleship.", code="self_invite")
    if not getattr(inviter, "has_employee_access", False) or not getattr(invitee, "has_employee_access", False):
        raise BattleshipRuleError(
            "Only active employees can play Battleship.",
            status=403,
            code="employee_only",
        )
    ensure_actions_allowed(now=current_time)

    pair_open_match = BattleshipMatch.objects.filter(
        inviter__in=[inviter, invitee],
        invitee__in=[inviter, invitee],
        status__in=OPEN_MATCH_STATUSES,
    ).exists()
    if pair_open_match:
        raise BattleshipRuleError(
            "There is already an open Battleship interaction between these two employees.",
            code="duplicate_pair_match",
        )

    match = BattleshipMatch.objects.create(
        inviter=inviter,
        invitee=invitee,
        invitation_expires_at=current_time + get_invitation_ttl(),
        last_activity_at=current_time,
        rematch_parent=rematch_parent,
    )
    BattleshipParticipant.objects.bulk_create(
        [
            BattleshipParticipant(match=match, user=inviter, slot=BattleshipParticipant.Slot.CHALLENGER),
            BattleshipParticipant(match=match, user=invitee, slot=BattleshipParticipant.Slot.OPPONENT),
        ]
    )
    create_event(
        match,
        BattleshipEvent.EventType.INVITE_SENT,
        f"{inviter.full_name} invited {invitee.full_name} to a Battleship match.",
        actor=inviter,
        metadata={"inviter_id": inviter.id, "invitee_id": invitee.id},
        request=request,
    )
    return get_match_queryset().get(pk=match.pk)


def load_match_for_viewer(match_id, viewer, *, now=None, request=None):
    match = get_match_queryset().get(pk=match_id)
    get_participant(match, viewer)
    sync_match_state(match, now=now, request=request)
    return get_match_queryset().get(pk=match.pk)


def respond_to_invitation(match_id, actor, decision, *, request=None, now=None):
    current_time = now or get_now()
    normalized = str(decision or "").strip().lower()
    if normalized not in {"accept", "decline"}:
        raise BattleshipRuleError("Decision must be accept or decline.", code="invalid_decision")

    with transaction.atomic():
        match = get_match_queryset().select_for_update().get(pk=match_id)
        sync_match_state(match, now=current_time, request=request)
        get_participant(match, actor)
        if actor.id != match.invitee_id:
            raise BattleshipRuleError(
                "Only the invited player can respond to this invitation.",
                status=403,
                code="invitee_only",
            )
        if match.status != BattleshipMatch.Status.INVITED:
            raise BattleshipRuleError(
                "This invitation is no longer waiting for a response.",
                status=409,
                code="invitation_closed",
            )

        if normalized == "decline":
            match.status = BattleshipMatch.Status.DECLINED
            match.responded_at = current_time
            match.last_activity_at = current_time
            match.save(update_fields=["status", "responded_at", "last_activity_at", "updated_at"])
            create_event(
                match,
                BattleshipEvent.EventType.INVITE_DECLINED,
                f"{actor.full_name} declined the Battleship invitation.",
                actor=actor,
                request=request,
            )
            return get_match_queryset().get(pk=match.pk)

        ensure_actions_allowed(match, now=current_time, request=request)
        claim_global_slot(match)
        match.status = BattleshipMatch.Status.SHIP_PLACEMENT
        match.responded_at = current_time
        match.accepted_at = current_time
        match.last_activity_at = current_time
        match.save(
            update_fields=[
                "status",
                "responded_at",
                "accepted_at",
                "last_activity_at",
                "occupies_global_slot",
                "updated_at",
            ]
        )
        create_event(
            match,
            BattleshipEvent.EventType.INVITE_ACCEPTED,
            f"{actor.full_name} accepted the Battleship invitation.",
            actor=actor,
            request=request,
        )
        sync_match_state(match, now=current_time, request=request)
        return get_match_queryset().get(pk=match.pk)


def cancel_invitation(match_id, actor, *, request=None, now=None):
    current_time = now or get_now()
    with transaction.atomic():
        match = get_match_queryset().select_for_update().get(pk=match_id)
        get_participant(match, actor)
        if actor.id != match.inviter_id:
            raise BattleshipRuleError(
                "Only the inviting player can cancel this invitation.",
                status=403,
                code="inviter_only",
            )
        sync_match_state(match, now=current_time, request=request)
        if match.status != BattleshipMatch.Status.INVITED:
            raise BattleshipRuleError(
                "Only pending invitations can be cancelled.",
                status=409,
                code="invitation_not_pending",
            )
        match.status = BattleshipMatch.Status.CANCELLED
        match.responded_at = current_time
        match.last_activity_at = current_time
        match.save(update_fields=["status", "responded_at", "last_activity_at", "updated_at"])
        create_event(
            match,
            BattleshipEvent.EventType.INVITE_CANCELLED,
            f"{actor.full_name} cancelled the Battleship invitation.",
            actor=actor,
            request=request,
        )
        return get_match_queryset().get(pk=match.pk)


def submit_fleet_layout(match_id, actor, layout, *, request=None, now=None):
    current_time = now or get_now()
    normalized_layout = validate_fleet_layout(layout)
    with transaction.atomic():
        match = get_match_queryset().select_for_update().get(pk=match_id)
        sync_match_state(match, now=current_time, request=request)
        participant = get_participant(match, actor)
        if match.status == BattleshipMatch.Status.PAUSED_OFFICE_HOURS:
            raise BattleshipRuleError(
                "Game paused due to office peak hours.",
                status=409,
                code="match_paused",
                extra={"office_policy": office_policy_payload(now=current_time)},
            )
        ensure_actions_allowed(match, now=current_time, request=request)
        if match.status != BattleshipMatch.Status.SHIP_PLACEMENT:
            raise BattleshipRuleError(
                "Ship placement is no longer available for this match.",
                status=409,
                code="placement_closed",
            )

        participant.fleet_layout = normalized_layout
        participant.placement_ready = True
        participant.ready_at = current_time
        participant.save(update_fields=["fleet_layout", "placement_ready", "ready_at", "updated_at"])
        create_event(
            match,
            BattleshipEvent.EventType.SHIPS_LOCKED,
            f"{actor.full_name} locked in their fleet.",
            actor=actor,
            metadata={"participant_id": participant.id},
            request=request,
        )

        all_ready = all(item.placement_ready for item in match.participants.all())
        match.last_activity_at = current_time
        update_fields = ["last_activity_at", "updated_at"]
        if all_ready:
            match.status = BattleshipMatch.Status.ACTIVE
            match.started_at = match.started_at or current_time
            match.turn_owner = choose_first_turn(match)
            update_fields.extend(["status", "started_at", "turn_owner"])
        match.save(update_fields=update_fields)

        if all_ready:
            create_event(
                match,
                BattleshipEvent.EventType.MATCH_STARTED,
                f"Battle started. {match.turn_owner.full_name} goes first.",
                actor=actor,
                metadata={"turn_owner_id": match.turn_owner_id},
                request=request,
            )
            sync_match_state(match, now=current_time, request=request)

        return get_match_queryset().get(pk=match.pk)


def fire_turn(match_id, actor, row, col, *, request=None, now=None):
    current_time = now or get_now()
    try:
        row = int(row)
        col = int(col)
    except (TypeError, ValueError) as exc:
        raise BattleshipRuleError("Shot coordinates must be valid integers.", code="invalid_coordinates") from exc
    if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE:
        raise BattleshipRuleError("Shot must stay within the 10x10 board.", code="invalid_coordinates")

    with transaction.atomic():
        match = get_match_queryset().select_for_update().get(pk=match_id)
        sync_match_state(match, now=current_time, request=request)
        participant = get_participant(match, actor)
        opponent = get_opponent_participant(match, participant)

        if match.status == BattleshipMatch.Status.PAUSED_OFFICE_HOURS:
            raise BattleshipRuleError(
                "Game paused due to office peak hours.",
                status=409,
                code="match_paused",
                extra={"office_policy": office_policy_payload(now=current_time)},
            )
        ensure_actions_allowed(match, now=current_time, request=request)
        if match.status != BattleshipMatch.Status.ACTIVE:
            raise BattleshipRuleError(
                "The match is not currently accepting turns.",
                status=409,
                code="match_not_active",
            )
        if match.turn_owner_id != actor.id:
            raise BattleshipRuleError(
                "It is not your turn yet.",
                status=409,
                code="not_your_turn",
            )
        if BattleshipShot.objects.filter(
            match=match,
            target_participant=opponent,
            row=row,
            col=col,
        ).exists():
            raise BattleshipRuleError(
                "That cell has already been targeted.",
                status=409,
                code="duplicate_target",
                extra={"cell": coordinate_label(row, col)},
            )

        outcome = resolve_shot(opponent, row, col)
        shot = BattleshipShot.objects.create(
            match=match,
            shooter=actor,
            target_participant=opponent,
            row=row,
            col=col,
            result=outcome["result"],
            ship_type=outcome["ship_type"],
            turn_number=match.total_turns + 1,
        )
        match.total_turns += 1
        match.last_activity_at = current_time
        match.inactive_player = None
        update_fields = ["total_turns", "last_activity_at", "inactive_player", "updated_at"]

        create_event(
            match,
            BattleshipEvent.EventType.SHOT_FIRED,
            f"{actor.full_name} fired at {coordinate_label(row, col)} for a {outcome['result']}.",
            actor=actor,
            metadata={
                "row": row,
                "col": col,
                "move_label": coordinate_label(row, col),
                "result": outcome["result"],
                "ship_type": outcome["ship_type"],
            },
            request=request,
        )

        if outcome["all_sunk"]:
            match.status = BattleshipMatch.Status.COMPLETED
            match.completed_at = current_time
            match.winner = actor
            match.loser = opponent.user
            match.turn_owner = None
            match.occupies_global_slot = False
            update_fields.extend(
                ["status", "completed_at", "winner", "loser", "turn_owner", "occupies_global_slot"]
            )
            create_event(
                match,
                BattleshipEvent.EventType.MATCH_COMPLETED,
                f"{actor.full_name} won the Battleship match in {match.total_turns} turns.",
                actor=actor,
                metadata={"winner_id": actor.id, "loser_id": opponent.user_id},
                request=request,
            )
        else:
            match.turn_owner = opponent.user
            update_fields.append("turn_owner")

        match.save(update_fields=update_fields)
        return get_match_queryset().get(pk=match.pk)


def resign_match(match_id, actor, *, request=None, now=None):
    current_time = now or get_now()
    with transaction.atomic():
        match = get_match_queryset().select_for_update().get(pk=match_id)
        get_participant(match, actor)
        sync_match_state(match, now=current_time, request=request)
        if match.status not in SERIOUS_MATCH_STATUSES:
            raise BattleshipRuleError(
                "Only live Battleship matches can be resigned.",
                status=409,
                code="resignation_not_available",
            )
        opponent = next(
            participant.user
            for participant in match.participants.all()
            if participant.user_id != actor.id
        )
        match.status = BattleshipMatch.Status.RESIGNED
        match.completed_at = current_time
        match.resigned_by = actor
        match.winner = opponent
        match.loser = actor
        match.turn_owner = None
        match.occupies_global_slot = False
        match.last_activity_at = current_time
        match.save(
            update_fields=[
                "status",
                "completed_at",
                "resigned_by",
                "winner",
                "loser",
                "turn_owner",
                "occupies_global_slot",
                "last_activity_at",
                "updated_at",
            ]
        )
        create_event(
            match,
            BattleshipEvent.EventType.MATCH_RESIGNED,
            f"{actor.full_name} resigned from the Battleship match.",
            actor=actor,
            metadata={"winner_id": opponent.id, "loser_id": actor.id},
            request=request,
        )
        return get_match_queryset().get(pk=match.pk)


def request_rematch(match_id, actor, *, request=None, now=None):
    current_time = now or get_now()
    with transaction.atomic():
        match = get_match_queryset().select_for_update().get(pk=match_id)
        get_participant(match, actor)
        sync_match_state(match, now=current_time, request=request)
        if match.status not in {
            BattleshipMatch.Status.COMPLETED,
            BattleshipMatch.Status.RESIGNED,
            BattleshipMatch.Status.ABANDONED,
        }:
            raise BattleshipRuleError(
                "Rematch is only available for finished Battleship games.",
                status=409,
                code="rematch_unavailable",
            )
        ensure_actions_allowed(now=current_time)
        opponent = next(
            participant.user
            for participant in match.participants.all()
            if participant.user_id != actor.id
        )
        rematch = create_invitation(
            actor,
            opponent,
            request=request,
            rematch_parent=match,
            now=current_time,
        )
        create_event(
            rematch,
            BattleshipEvent.EventType.REMATCH_REQUESTED,
            f"{actor.full_name} requested a rematch with {opponent.full_name}.",
            actor=actor,
            metadata={"parent_match_id": match.id},
            request=request,
        )
        return rematch


def get_candidate_users(*, viewer, query=""):
    queryset = User.objects.filter(
        is_active=True,
        employment_status=User.EmploymentStatus.ACTIVE,
        access_level__in=EMPLOYEE_ACCESS_LEVELS,
    ).exclude(pk=viewer.id)
    if query:
        queryset = queryset.filter(
            models.Q(display_name__icontains=query)
            | models.Q(first_name__icontains=query)
            | models.Q(last_name__icontains=query)
            | models.Q(email__icontains=query)
            | models.Q(title__icontains=query)
            | models.Q(location__icontains=query)
            | models.Q(department__icontains=query)
        )
    return list(queryset.order_by("display_name", "first_name", "email")[:12])


def sync_relevant_matches_for_user(user, *, request=None, now=None):
    relevant_matches = get_match_queryset().filter(
        participants__user=user,
        status__in=OPEN_MATCH_STATUSES | {
            BattleshipMatch.Status.COMPLETED,
            BattleshipMatch.Status.RESIGNED,
            BattleshipMatch.Status.ABANDONED,
        },
    )[:10]
    for match in relevant_matches:
        sync_match_state(match, now=now, request=request)
