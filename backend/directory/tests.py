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
            department_for_connect="Rating Operations",
            expertise="Infrastructure ratings",
            skills=["credit", "surveillance"],
        )

        response = self.client.get("/api/directory/", {"q": "Rahul"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["results"][0]["email"], "rahul.mehta@acuite.in")

    def test_directory_filters_include_company_department_function_and_location(self):
        user = User.objects.create_user(
            email="chitra.mohan@acuite.in",
            first_name="Chitra",
            last_name="Mohan",
            title="Vice President - Compliance",
            department="Compliance",
            location="Mumbai",
        )
        DirectoryProfile.objects.create(
            user=user,
            company_name="Acuite",
            function_name="Corporate",
            department_for_connect="Corporate",
            city="Mumbai",
            office_location="Mumbai",
            mobile_number="9819960324",
        )

        response = self.client.get("/api/directory/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["filters"]["company"], ["Acuite"])
        self.assertEqual(payload["filters"]["department"], ["Corporate"])
        self.assertEqual(payload["filters"]["function"], ["Corporate"])
        self.assertEqual(payload["filters"]["location"], ["Mumbai"])

    def test_directory_can_filter_by_department_for_connect(self):
        corporate_user = User.objects.create_user(
            email="chitra.mohan@acuite.in",
            first_name="Chitra",
            last_name="Mohan",
            title="Vice President - Compliance",
            department="Compliance",
            location="Mumbai",
        )
        ops_user = User.objects.create_user(
            email="rahul.mehta@acuite.in",
            first_name="Rahul",
            last_name="Mehta",
            title="Senior Analyst",
            department="Technology",
            location="Mumbai",
        )
        DirectoryProfile.objects.create(
            user=corporate_user,
            company_name="Acuite",
            department_for_connect="Corporate",
            city="Mumbai",
            office_location="Mumbai",
        )
        DirectoryProfile.objects.create(
            user=ops_user,
            company_name="Acuite",
            department_for_connect="Rating Operations",
            city="Mumbai",
            office_location="Mumbai",
        )

        response = self.client.get("/api/directory/", {"department": "Corporate"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["results"][0]["email"], "chitra.mohan@acuite.in")

# Create your tests here.
