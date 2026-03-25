from django.utils import timezone

from .models import BattleshipMatch, BattleshipParticipant, BattleshipShot
from .services import (
    FLEET_BY_TYPE,
    fleet_spec_payload,
    format_move_summary,
    get_inactive_deadline,
    get_opponent_participant,
    get_participant,
    office_policy_payload,
    ship_cells_by_type,
)


def serialize_candidate(user):
    return {
        "id": user.id,
        "name": user.full_name,
        "email": user.email,
        "title": user.title,
        "department": user.department,
        "location": user.location,
        "initials": user.initials,
    }


def serialize_match_brief(match, *, viewer=None, include_players=True):
    players = {}
    if include_players:
        players = {
            "inviter": serialize_candidate(match.inviter),
            "invitee": serialize_candidate(match.invitee),
        }
    return {
        "id": match.id,
        "status": match.status,
        "status_label": match.get_status_display(),
        "occupies_global_slot": match.occupies_global_slot,
        "paused_from_status": match.paused_from_status,
        "players": players,
        "turn_owner_id": match.turn_owner_id,
        "winner_id": match.winner_id,
        "loser_id": match.loser_id,
        "total_turns": match.total_turns,
        "rematch_parent_id": match.rematch_parent_id,
        "created_at": match.created_at.isoformat(),
        "started_at": match.started_at.isoformat() if match.started_at else None,
        "completed_at": match.completed_at.isoformat() if match.completed_at else None,
        "invitation_expires_at": (
            match.invitation_expires_at.isoformat() if match.invitation_expires_at else None
        ),
        "viewer_is_player": bool(
            viewer
            and getattr(viewer, "is_authenticated", False)
            and viewer.id in {match.inviter_id, match.invitee_id}
        ),
    }


def _serialize_event(event):
    metadata = event.metadata or {}
    move_label = metadata.get("move_label") or ""
    return {
        "id": event.id,
        "event_type": event.event_type,
        "summary": event.summary,
        "move_label": move_label,
        "created_at": event.created_at.isoformat(),
        "created_at_label": timezone.localtime(event.created_at).strftime("%d %b, %I:%M %p"),
        "actor_name": event.actor.full_name if event.actor else "",
    }


def _serialize_shot(shot):
    return {
        "id": shot.id,
        "row": shot.row,
        "col": shot.col,
        "label": f"{chr(65 + shot.row)}{shot.col + 1}",
        "result": shot.result,
        "ship_type": shot.ship_type,
        "turn_number": shot.turn_number,
        "created_at": shot.created_at.isoformat(),
        "summary": format_move_summary(shot),
    }


def _participant_ship_payload(participant):
    shots = list(
        BattleshipShot.objects.filter(target_participant=participant).order_by("turn_number")
    )
    shots_by_cell = {(shot.row, shot.col): shot for shot in shots}
    cells_by_ship = ship_cells_by_type(participant.fleet_layout or [])
    ships = []
    for ship in participant.fleet_layout or []:
        ship_type = ship["ship_type"]
        cells = ship.get("cells", [])
        hit_cells = [
            {
                **cell,
                "hit": (cell["row"], cell["col"]) in shots_by_cell,
                "result": shots_by_cell[(cell["row"], cell["col"])].result
                if (cell["row"], cell["col"]) in shots_by_cell
                else "",
            }
            for cell in cells
        ]
        all_hit = {(cell["row"], cell["col"]) for cell in cells} <= {
            (shot.row, shot.col)
            for shot in shots
            if shot.ship_type == ship_type and shot.result in {BattleshipShot.Result.HIT, BattleshipShot.Result.SUNK}
        }
        ships.append(
            {
                **ship,
                "sunk": all_hit and bool(cells_by_ship.get(ship_type)),
                "cells": hit_cells,
            }
        )
    return {
        "ships": ships,
        "shots_received": [_serialize_shot(shot) for shot in shots],
        "placement_ready": participant.placement_ready,
    }


def _tracking_board_payload(match, shooter, target_participant):
    shots = list(
        BattleshipShot.objects.filter(match=match, shooter=shooter).order_by("turn_number")
    )
    shot_cells = {(shot.row, shot.col): shot for shot in shots}
    revealed_sunk_cells = []
    sunk_ship_types = []
    for ship in target_participant.fleet_layout or []:
        cells = ship.get("cells", [])
        if cells and all((cell["row"], cell["col"]) in shot_cells for cell in cells):
            sunk_ship_types.append(ship["ship_type"])
            revealed_sunk_cells.extend(
                {
                    "row": cell["row"],
                    "col": cell["col"],
                    "label": cell.get("label") or f"{chr(65 + cell['row'])}{cell['col'] + 1}",
                    "ship_type": ship["ship_type"],
                }
                for cell in cells
            )
    return {
        "shots": [_serialize_shot(shot) for shot in shots],
        "target_player_id": target_participant.user_id,
        "revealed_sunk_cells": revealed_sunk_cells,
        "sunk_ship_types": sunk_ship_types,
    }


def _turn_status(match, viewer, viewer_participant, opponent_participant, office_policy):
    if match.status == BattleshipMatch.Status.INVITED:
        if viewer.id == match.invitee_id:
            return "Invitation received. Accept or decline to continue."
        return "Invitation sent. Waiting for the other player."
    if match.status == BattleshipMatch.Status.SHIP_PLACEMENT:
        if viewer_participant.placement_ready:
            if opponent_participant.placement_ready:
                return "Both fleets are locked. Battle will begin shortly."
            return "Your fleet is locked. Waiting for your opponent to finish placement."
        return "Place your fleet on the board."
    if match.status == BattleshipMatch.Status.PAUSED_OFFICE_HOURS:
        return "Game paused due to office peak hours."
    if match.status == BattleshipMatch.Status.ACTIVE:
        if match.turn_owner_id == viewer.id:
            return "Your turn. Fire exactly one shot."
        return "Waiting for your opponent."
    if match.status == BattleshipMatch.Status.COMPLETED:
        return "You won the match." if match.winner_id == viewer.id else "You lost the match."
    if match.status == BattleshipMatch.Status.RESIGNED:
        return "You resigned from the match." if match.resigned_by_id == viewer.id else "Your opponent resigned."
    if match.status == BattleshipMatch.Status.ABANDONED:
        if match.inactive_player_id == viewer.id:
            return "The match was closed after inactivity on your side."
        return "The match was closed after opponent inactivity."
    if match.status == BattleshipMatch.Status.DECLINED:
        return "The invitation was declined."
    if match.status == BattleshipMatch.Status.EXPIRED:
        return "The invitation expired before it was accepted."
    if match.status == BattleshipMatch.Status.CANCELLED:
        return "The invitation was cancelled."
    return office_policy["message"]


def serialize_match_for_viewer(match, viewer):
    viewer_participant = get_participant(match, viewer)
    opponent_participant = get_opponent_participant(match, viewer_participant)
    office_policy = office_policy_payload()
    inactive_deadline = get_inactive_deadline(match)
    duration_seconds = 0
    if match.started_at:
        duration_end = match.completed_at or timezone.now()
        duration_seconds = int((duration_end - match.started_at).total_seconds())

    missing_ship_types = [
        ship["ship_type"]
        for ship in fleet_spec_payload()
        if ship["ship_type"] not in {item["ship_type"] for item in (viewer_participant.fleet_layout or [])}
    ]
    can_accept = (
        match.status == BattleshipMatch.Status.INVITED
        and viewer.id == match.invitee_id
        and not office_policy["blocked"]
    )
    can_decline = match.status == BattleshipMatch.Status.INVITED and viewer.id == match.invitee_id
    can_cancel = match.status == BattleshipMatch.Status.INVITED and viewer.id == match.inviter_id
    can_place_ships = (
        match.status == BattleshipMatch.Status.SHIP_PLACEMENT
        and not office_policy["blocked"]
        and not viewer_participant.placement_ready
    )
    can_fire = (
        match.status == BattleshipMatch.Status.ACTIVE
        and match.turn_owner_id == viewer.id
        and not office_policy["blocked"]
    )
    can_resign = match.status in BattleshipMatch.serious_statuses()
    can_rematch = (
        match.status
        in {
            BattleshipMatch.Status.COMPLETED,
            BattleshipMatch.Status.RESIGNED,
            BattleshipMatch.Status.ABANDONED,
        }
        and not office_policy["blocked"]
    )

    return {
        **serialize_match_brief(match, viewer=viewer),
        "phase_label": match.get_status_display(),
        "turn_status": _turn_status(match, viewer, viewer_participant, opponent_participant, office_policy),
        "office_policy": office_policy,
        "duration_seconds": duration_seconds,
        "inactive_deadline_at": inactive_deadline.isoformat() if inactive_deadline else None,
        "last_activity_at": match.last_activity_at.isoformat() if match.last_activity_at else None,
        "fleet_spec": fleet_spec_payload(),
        "viewer": {
            "id": viewer.id,
            "participant_id": viewer_participant.id,
            "name": viewer.full_name,
            "initials": viewer.initials,
            "placement_ready": viewer_participant.placement_ready,
            "missing_ship_types": missing_ship_types,
            "can_accept": can_accept,
            "can_decline": can_decline,
            "can_cancel": can_cancel,
            "can_place_ships": can_place_ships,
            "can_fire": can_fire,
            "can_resign": can_resign,
            "can_rematch": can_rematch,
        },
        "opponent": {
            "id": opponent_participant.user.id,
            "participant_id": opponent_participant.id,
            "name": opponent_participant.user.full_name,
            "initials": opponent_participant.user.initials,
            "title": opponent_participant.user.title,
            "placement_ready": opponent_participant.placement_ready,
        },
        "winner": serialize_candidate(match.winner) if match.winner else None,
        "loser": serialize_candidate(match.loser) if match.loser else None,
        "own_board": _participant_ship_payload(viewer_participant),
        "target_board": _tracking_board_payload(match, viewer, opponent_participant),
        "history": [_serialize_event(event) for event in match.events.all().order_by("-created_at")[:40]],
    }
