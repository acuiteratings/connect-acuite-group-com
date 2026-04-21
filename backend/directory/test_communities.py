from django.test import TestCase

from accounts.models import User

from .models import DirectoryProfile


class CommunityApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="community.member@acuite.in",
            first_name="Community",
            last_name="Member",
            title="Analyst",
            department="Technology",
            location="Mumbai",
        )
        self.other_user = User.objects.create_user(
            email="second.member@acuite.in",
            first_name="Second",
            last_name="Member",
            title="Analyst",
            department="Technology",
            location="Mumbai",
        )

    def test_communities_endpoint_lists_clubs_and_member_counts(self):
        DirectoryProfile.objects.create(
            user=self.user,
            office_location="Mumbai",
            city="Mumbai",
            clubs=["reading_club", "travel_club"],
        )
        DirectoryProfile.objects.create(
            user=self.other_user,
            office_location="Mumbai",
            city="Mumbai",
            clubs=["reading_club"],
        )
        self.client.force_login(self.user)

        response = self.client.get("/api/directory/communities/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 12)
        self.assertEqual(payload["joined_count"], 2)
        reading_club = next(item for item in payload["results"] if item["key"] == "reading_club")
        self.assertEqual(reading_club["member_count"], 2)
        self.assertTrue(reading_club["joined"])

    def test_employee_can_join_and_leave_a_community(self):
        self.client.force_login(self.user)

        join_response = self.client.post(
            "/api/directory/communities/",
            data='{"club_key":"technology_club","action":"join"}',
            content_type="application/json",
        )

        self.assertEqual(join_response.status_code, 200)
        payload = join_response.json()
        self.assertEqual(payload["joined_count"], 1)
        technology_club = next(item for item in payload["results"] if item["key"] == "technology_club")
        self.assertTrue(technology_club["joined"])
        self.assertEqual(technology_club["member_count"], 1)

        leave_response = self.client.post(
            "/api/directory/communities/",
            data='{"club_key":"technology_club","action":"leave"}',
            content_type="application/json",
        )

        self.assertEqual(leave_response.status_code, 200)
        payload = leave_response.json()
        self.assertEqual(payload["joined_count"], 0)
        technology_club = next(item for item in payload["results"] if item["key"] == "technology_club")
        self.assertFalse(technology_club["joined"])
        self.assertEqual(technology_club["member_count"], 0)
