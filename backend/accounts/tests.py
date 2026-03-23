from django.test import TestCase


class CurrentUserApiTests(TestCase):
    def test_me_endpoint_returns_unauthenticated_payload_for_anonymous_request(self):
        response = self.client.get("/api/accounts/me/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertFalse(payload["authenticated"])
        self.assertIn("email_otp", payload["next_auth_decision"])

# Create your tests here.
