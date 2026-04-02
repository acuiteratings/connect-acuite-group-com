import json
from datetime import timedelta
from unittest import mock

from django.test import TestCase
from django.utils import timezone

from accounts.models import User

from .models import QuizMatch, QuizParticipant


class QuizApiTests(TestCase):
    def setUp(self):
        self.host = User.objects.create_user(
            email="host@acuite.in",
            password="testpass123",
            first_name="Quiz",
            last_name="Host",
            access_level=User.AccessLevel.ADMIN,
            must_change_password=False,
        )
        self.player_two = User.objects.create_user(
            email="player.two@acuite.in",
            password="testpass123",
            first_name="Player",
            last_name="Two",
            must_change_password=False,
        )
        self.player_three = User.objects.create_user(
            email="player.three@acuite.in",
            password="testpass123",
            first_name="Player",
            last_name="Three",
            must_change_password=False,
        )

    def test_host_can_create_quiz_invite(self):
        self.client.force_login(self.host)
        response = self.client.post(
            "/api/quiz/matches/",
            data=json.dumps(
                {
                    "difficulty": "amateur",
                    "invitee_user_ids": [self.player_two.id, self.player_three.id],
                }
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(QuizMatch.objects.count(), 1)
        self.assertEqual(QuizParticipant.objects.filter(match__host=self.host).count(), 3)

    def test_invited_player_can_accept_and_host_can_start(self):
        self.client.force_login(self.host)
        create_response = self.client.post(
            "/api/quiz/matches/",
            data=json.dumps({"difficulty": "amateur", "invitee_user_ids": [self.player_two.id]}),
            content_type="application/json",
        )
        match_id = create_response.json()["match"]["id"]

        self.client.force_login(self.player_two)
        accept_response = self.client.post(
            f"/api/quiz/matches/{match_id}/respond/",
            data=json.dumps({"decision": "accept"}),
            content_type="application/json",
        )
        self.assertEqual(accept_response.status_code, 200)

        self.client.force_login(self.host)
        start_response = self.client.post(f"/api/quiz/matches/{match_id}/start/")
        self.assertEqual(start_response.status_code, 200)
        self.assertEqual(start_response.json()["match"]["status"], QuizMatch.Status.ACTIVE)
        self.assertEqual(len(start_response.json()["match"]["current_question"]["options"]), 4)

    def test_answer_scores_point_for_correct_option(self):
        self.client.force_login(self.host)
        match_id = self.client.post(
            "/api/quiz/matches/",
            data=json.dumps({"difficulty": "amateur", "invitee_user_ids": [self.player_two.id]}),
            content_type="application/json",
        ).json()["match"]["id"]
        self.client.force_login(self.player_two)
        self.client.post(
            f"/api/quiz/matches/{match_id}/respond/",
            data=json.dumps({"decision": "accept"}),
            content_type="application/json",
        )
        self.client.force_login(self.host)
        start_payload = self.client.post(f"/api/quiz/matches/{match_id}/start/").json()["match"]
        correct_option = None
        from .question_bank import get_question_by_key

        correct_option = get_question_by_key(start_payload["current_question"]["key"])["correct_option"]
        answer_response = self.client.post(
            f"/api/quiz/matches/{match_id}/answer/",
            data=json.dumps({"selected_option": correct_option}),
            content_type="application/json",
        )
        self.assertEqual(answer_response.status_code, 200)
        host_participant = QuizParticipant.objects.get(match_id=match_id, user=self.host)
        self.assertEqual(host_participant.score, 1)

    def test_state_advances_after_deadline(self):
        self.client.force_login(self.host)
        match_id = self.client.post(
            "/api/quiz/matches/",
            data=json.dumps({"difficulty": "amateur", "invitee_user_ids": [self.player_two.id]}),
            content_type="application/json",
        ).json()["match"]["id"]
        self.client.force_login(self.player_two)
        self.client.post(
            f"/api/quiz/matches/{match_id}/respond/",
            data=json.dumps({"decision": "accept"}),
            content_type="application/json",
        )
        self.client.force_login(self.host)
        self.client.post(f"/api/quiz/matches/{match_id}/start/")
        match = QuizMatch.objects.get(pk=match_id)
        future_now = match.question_deadline_at + timedelta(seconds=1)
        with mock.patch("quiz.services.timezone.now", return_value=future_now), mock.patch(
            "quiz.serializers.timezone.now",
            return_value=future_now,
        ):
            response = self.client.get(f"/api/quiz/matches/{match_id}/state/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["match"]["current_question"]["index"], 2)
