from datetime import datetime, timedelta
from unittest import mock
from zoneinfo import ZoneInfo

from django.test import TestCase, override_settings
from django.utils import timezone

from accounts.services import SESSION_AUTH_BACKEND
from accounts.models import User

from .models import BattleshipMatch, BattleshipShot
from .services import (
    BattleshipRuleError,
    create_invitation,
    fire_turn,
    respond_to_invitation,
    submit_fleet_layout,
    sync_match_state,
    validate_fleet_layout,
)


@override_settings(
    BATTLESHIP_TIMEZONE="Asia/Kolkata",
    BATTLESHIP_BLOCK_WINDOWS=[("10:00", "13:00"), ("14:00", "18:30")],
    BATTLESHIP_INACTIVITY_TIMEOUT_MINUTES=30,
)
class BattleshipServiceTests(TestCase):
    def setUp(self):
        self.tz = ZoneInfo("Asia/Kolkata")
        self.alice = self.make_user("alice@acuite.in", "Alice Analyst")
        self.bob = self.make_user("bob@acuite.in", "Bob Reviewer")
        self.charlie = self.make_user("charlie@acuite.in", "Charlie Ops")
        self.diana = self.make_user("diana@acuite.in", "Diana Markets")

    def make_user(self, email, name):
        first_name, last_name = name.split(" ", 1)
        return User.objects.create_user(
            email=email,
            password="Pass123!pass",
            first_name=first_name,
            last_name=last_name,
            display_name=name,
            employment_status=User.EmploymentStatus.ACTIVE,
            access_level=User.AccessLevel.EMPLOYEE,
            must_change_password=False,
            password_changed_at=timezone.now(),
        )

    def make_time(self, hour, minute=0):
        return timezone.make_aware(datetime(2026, 3, 25, hour, minute), self.tz)

    def valid_layout(self):
        return [
            {"ship_type": "carrier", "row": 0, "col": 0, "orientation": "horizontal"},
            {"ship_type": "battleship", "row": 2, "col": 0, "orientation": "horizontal"},
            {"ship_type": "cruiser", "row": 4, "col": 0, "orientation": "horizontal"},
            {"ship_type": "submarine", "row": 6, "col": 0, "orientation": "horizontal"},
            {"ship_type": "destroyer", "row": 8, "col": 0, "orientation": "horizontal"},
        ]

    def tight_layout(self):
        return [
            {"ship_type": "carrier", "row": 0, "col": 0, "orientation": "vertical"},
            {"ship_type": "battleship", "row": 0, "col": 2, "orientation": "vertical"},
            {"ship_type": "cruiser", "row": 0, "col": 4, "orientation": "vertical"},
            {"ship_type": "submarine", "row": 0, "col": 6, "orientation": "vertical"},
            {"ship_type": "destroyer", "row": 0, "col": 8, "orientation": "vertical"},
        ]

    def start_active_match(self, *, challenger=None, opponent=None, now=None):
        challenger = challenger or self.alice
        opponent = opponent or self.bob
        now = now or self.make_time(8, 0)
        invite = create_invitation(challenger, opponent, now=now)
        accepted = respond_to_invitation(invite.id, opponent, "accept", now=now + timedelta(minutes=1))
        with mock.patch("battleship.services.secrets.randbelow", return_value=0):
            submit_fleet_layout(
                accepted.id,
                challenger,
                self.valid_layout(),
                now=now + timedelta(minutes=2),
            )
            active = submit_fleet_layout(
                accepted.id,
                opponent,
                self.tight_layout(),
                now=now + timedelta(minutes=3),
            )
        active.refresh_from_db()
        return active

    def test_validate_fleet_layout_rejects_overlap(self):
        overlapping_layout = self.valid_layout()
        overlapping_layout[1] = {
            "ship_type": "battleship",
            "row": 0,
            "col": 0,
            "orientation": "vertical",
        }
        with self.assertRaises(BattleshipRuleError) as exc:
            validate_fleet_layout(overlapping_layout)
        self.assertEqual(exc.exception.code, "ship_overlap")

    def test_acceptance_is_blocked_during_peak_hours(self):
        invite = create_invitation(self.alice, self.bob, now=self.make_time(8, 30))
        with self.assertRaises(BattleshipRuleError) as exc:
            respond_to_invitation(invite.id, self.bob, "accept", now=self.make_time(10, 5))
        self.assertEqual(exc.exception.code, "office_hours_blocked")
        invite.refresh_from_db()
        self.assertEqual(invite.status, BattleshipMatch.Status.INVITED)

    def test_one_active_match_slot_is_enforced(self):
        first_invite = create_invitation(self.alice, self.bob, now=self.make_time(8, 0))
        first_match = respond_to_invitation(first_invite.id, self.bob, "accept", now=self.make_time(8, 5))
        first_match.refresh_from_db()
        self.assertTrue(first_match.occupies_global_slot)

        second_invite = create_invitation(self.charlie, self.diana, now=self.make_time(8, 10))
        with self.assertRaises(BattleshipRuleError) as exc:
            respond_to_invitation(second_invite.id, self.diana, "accept", now=self.make_time(8, 15))
        self.assertEqual(exc.exception.code, "global_slot_occupied")

    def test_match_pauses_and_resumes_across_block_windows(self):
        active = self.start_active_match(now=self.make_time(8, 0))
        active = sync_match_state(active, now=self.make_time(10, 0))
        self.assertEqual(active.status, BattleshipMatch.Status.PAUSED_OFFICE_HOURS)
        self.assertEqual(active.paused_from_status, BattleshipMatch.Status.ACTIVE)

        active = sync_match_state(active, now=self.make_time(13, 1))
        self.assertEqual(active.status, BattleshipMatch.Status.ACTIVE)
        self.assertEqual(active.paused_from_status, "")

    def test_duplicate_turn_is_rejected(self):
        active = self.start_active_match(now=self.make_time(8, 0))
        self.assertEqual(active.turn_owner_id, self.alice.id)
        fire_turn(active.id, self.alice, 0, 0, now=self.make_time(8, 10))
        with self.assertRaises(BattleshipRuleError) as exc:
            fire_turn(active.id, self.alice, 0, 1, now=self.make_time(8, 11))
        self.assertEqual(exc.exception.code, "not_your_turn")

    def test_all_sunk_declares_winner_and_finishes_match(self):
        active = self.start_active_match(now=self.make_time(8, 0))
        # Alice starts first because randbelow is patched to 0 in start_active_match.
        target_sequence = [
            (0, 0),
            (0, 2),
            (0, 4),
            (0, 6),
            (0, 8),
            (1, 0),
            (1, 2),
            (1, 4),
            (1, 6),
            (1, 8),
            (2, 0),
            (2, 2),
            (2, 4),
            (3, 0),
            (3, 2),
            (4, 0),
            (2, 6),
        ]
        reply_sequence = [
            (9, 9),
            (9, 8),
            (9, 7),
            (9, 6),
            (9, 5),
            (9, 4),
            (9, 3),
            (9, 2),
            (9, 1),
            (8, 9),
            (8, 8),
            (8, 7),
            (8, 6),
            (8, 5),
            (8, 4),
            (8, 3),
        ]

        now = self.make_time(8, 10)
        for index, shot in enumerate(target_sequence):
            active = fire_turn(active.id, self.alice, shot[0], shot[1], now=now + timedelta(minutes=index * 2))
            active.refresh_from_db()
            if active.status == BattleshipMatch.Status.COMPLETED:
                break
            reply = reply_sequence[index]
            active = fire_turn(active.id, self.bob, reply[0], reply[1], now=now + timedelta(minutes=index * 2 + 1))
            active.refresh_from_db()

        self.assertEqual(active.status, BattleshipMatch.Status.COMPLETED)
        self.assertEqual(active.winner_id, self.alice.id)
        self.assertEqual(active.loser_id, self.bob.id)
        self.assertFalse(active.occupies_global_slot)
        self.assertTrue(BattleshipShot.objects.filter(match=active).exists())

    def test_inactivity_abandons_match(self):
        active = self.start_active_match(now=self.make_time(8, 0))
        active.last_activity_at = self.make_time(8, 5)
        active.turn_owner = self.alice
        active.save(update_fields=["last_activity_at", "turn_owner", "updated_at"])
        active = sync_match_state(active, now=self.make_time(8, 36))
        self.assertEqual(active.status, BattleshipMatch.Status.ABANDONED)
        self.assertEqual(active.inactive_player_id, self.alice.id)
        self.assertEqual(active.winner_id, self.bob.id)

    def test_non_participant_cannot_access_match_state_endpoint(self):
        active = self.start_active_match(now=self.make_time(8, 0))
        outsider = self.make_user("outsider@acuite.in", "Outside Viewer")
        self.client.force_login(outsider, backend=SESSION_AUTH_BACKEND)
        response = self.client.get(f"/api/battleship/matches/{active.id}/state/")
        self.assertEqual(response.status_code, 403)
