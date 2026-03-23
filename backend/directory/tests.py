from django.test import TestCase

from accounts.models import User

from .models import DirectoryProfile


class DirectoryApiTests(TestCase):
    def test_directory_search_returns_matching_profile(self):
        user = User.objects.create_user(
            email="rahul.mehta@acuite.in",
            first_name="Rahul",
            last_name="Mehta",
            title="Senior Analyst",
            department="Ratings",
            location="Mumbai",
        )
        DirectoryProfile.objects.create(
            user=user,
            city="Mumbai",
            office_location="Head Office",
            expertise="Infrastructure ratings",
            skills=["credit", "surveillance"],
        )

        response = self.client.get("/api/directory/", {"q": "Rahul"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["results"][0]["email"], "rahul.mehta@acuite.in")

# Create your tests here.
