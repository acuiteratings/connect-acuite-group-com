from datetime import datetime, timedelta
from unittest import mock
from zoneinfo import ZoneInfo

from django.test import TestCase, override_settings
from django.utils import timezone

from accounts.models import User
from accounts.services import SESSION_AUTH_BACKEND

from .models import BattleshipMatch
from .services import create_invitation, respond_to_invitation, submit_fleet_layout


@override_settings(
    BATTLESHIP_TIMEZONE="Asia/Kolkata",
    BATTLESHIP_BLOCK_WINDOWS=[("10:00", "13:00"), ("14:00", "18:30")],
    BATTLESHIP_INACTIVITY_TIMEOUT_MINUTES=30,
)
class BattleshipGlobalSlotViewTests(TestCase):
    def setUp(self):
        self.tz = ZoneInfo("Asia/Kolkata")
        self.alice = self.make_user("alice@acuite.in", "Alice Analyst")
        self.bob = self.make_user("bob@acuite.in", "Bob Reviewer")
        self.charlie = self.make_user("charlie@acuite.in", "Charlie Ops")

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

    def start_active_match(self, *, now):
        invite = create_invitation(self.alice, self.bob, now=now)
        accepted = respond_to_invitation(invite.id, self.bob, "accept", now=now + timedelta(minutes=1))
        with mock.patch("battleship.services.secrets.randbelow", return_value=0):
            submit_fleet_layout(accepted.id, self.alice, self.valid_layout(), now=now + timedelta(minutes=2))
            active = submit_fleet_layout(accepted.id, self.bob, self.tight_layout(), now=now + timedelta(minutes=3))
        active.refresh_from_db()
        return active

    def test_lobby_releases_stale_global_slot_for_other_employees(self):
        stale_match = self.start_active_match(now=self.make_time(8, 0))
        stale_match.last_activity_at = self.make_time(8, 5)
        stale_match.turn_owner = self.alice
        stale_match.save(update_fields=["last_activity_at", "turn_owner", "updated_at"])

        self.client.force_login(self.charlie, backend=SESSION_AUTH_BACKEND)
        with mock.patch("battleship.services.get_now", return_value=self.make_time(8, 36)):
            response = self.client.get("/api/battleship/lobby/")

        self.assertEqual(response.status_code, 200)
        stale_match.refresh_from_db()
        self.assertEqual(stale_match.status, BattleshipMatch.Status.ABANDONED)
        self.assertFalse(stale_match.occupies_global_slot)
        self.assertEqual(stale_match.inactive_player_id, self.alice.id)
        self.assertIsNone(response.json()["global_active_match"])
