import json

from django.test import TestCase

from accounts.models import User

from .models import Poll, PollOption, PollVote


class VoicePollApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="voice.user@acuite.in",
            password="testpass123",
            first_name="Voice",
            last_name="User",
        )
        self.poll = Poll.objects.create(question="What should Connect prioritize next?")
        self.option_one = PollOption.objects.create(poll=self.poll, label="Ideas board", position=1)
        self.option_two = PollOption.objects.create(poll=self.poll, label="Brand Store", position=2)

    def test_active_poll_endpoint_returns_poll(self):
        response = self.client.get("/api/voice/polls/active/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["poll"]["question"], "What should Connect prioritize next?")
        self.assertEqual(len(payload["poll"]["options"]), 2)

    def test_authenticated_user_can_vote_on_active_poll(self):
        self.client.force_login(self.user)

        response = self.client.post(
            f"/api/voice/polls/{self.poll.id}/vote/",
            data=json.dumps({"option_id": self.option_one.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["poll"]["user_vote_option_id"], self.option_one.id)
        self.assertEqual(PollVote.objects.count(), 1)

    def test_vote_updates_existing_vote(self):
        PollVote.objects.create(poll=self.poll, option=self.option_one, voter=self.user)
        self.client.force_login(self.user)

        response = self.client.post(
            f"/api/voice/polls/{self.poll.id}/vote/",
            data=json.dumps({"option_id": self.option_two.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(PollVote.objects.count(), 1)
        self.assertEqual(PollVote.objects.get().option_id, self.option_two.id)

