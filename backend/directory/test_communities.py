from django.test import TestCase

from accounts.models import User

from .models import CommunityMembership, DirectoryProfile


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
        )
        DirectoryProfile.objects.create(
            user=self.other_user,
            office_location="Mumbai",
            city="Mumbai",
        )
        CommunityMembership.objects.create(
            user=self.user,
            club_key="reading_club",
            is_admin=True,
        )
        CommunityMembership.objects.create(
            user=self.user,
            club_key="travel_club",
        )
        CommunityMembership.objects.create(
            user=self.other_user,
            club_key="reading_club",
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
        self.assertTrue(reading_club["viewer_is_admin"])
        self.assertEqual(reading_club["club_admin"]["name"], self.user.full_name)

    def test_first_member_to_join_becomes_club_admin(self):
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
        self.assertTrue(technology_club["viewer_is_admin"])
        self.assertEqual(technology_club["club_admin"]["name"], self.user.full_name)

    def test_next_member_becomes_admin_when_previous_admin_leaves(self):
        first_profile = DirectoryProfile.objects.create(
            user=self.user,
            office_location="Mumbai",
            city="Mumbai",
        )
        second_profile = DirectoryProfile.objects.create(
            user=self.other_user,
            office_location="Mumbai",
            city="Mumbai",
        )
        CommunityMembership.objects.create(
            user=self.user,
            club_key="technology_club",
            is_admin=True,
        )
        CommunityMembership.objects.create(
            user=self.other_user,
            club_key="technology_club",
            is_admin=False,
        )
        first_profile.clubs = ["technology_club"]
        first_profile.save(update_fields=["clubs", "updated_at"])
        second_profile.clubs = ["technology_club"]
        second_profile.save(update_fields=["clubs", "updated_at"])
        self.client.force_login(self.user)

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
        self.assertEqual(technology_club["member_count"], 1)
        self.assertEqual(technology_club["club_admin"]["name"], self.other_user.full_name)
        self.assertTrue(
            CommunityMembership.objects.get(
                user=self.other_user,
                club_key="technology_club",
            ).is_admin
        )
