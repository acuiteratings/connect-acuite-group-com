from unittest.mock import patch

from django.test import TestCase

from accounts.models import User

from .models import DirectoryProfile


class DirectoryApiTests(TestCase):
    def test_directory_skips_coin_expiry_refresh_work(self):
        user = User.objects.create_user(
            email="fast.directory@acuite.in",
            first_name="Fast",
            last_name="Directory",
            title="Analyst",
            department="Technology",
            location="Mumbai",
        )
        DirectoryProfile.objects.create(
            user=user,
            city="Mumbai",
            office_location="Mumbai",
            department_for_connect="Rating Operations",
        )

        with patch("directory.views.build_coin_balance_map", return_value={user.id: {}}) as mocked_balance_map:
            response = self.client.get("/api/directory/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(mocked_balance_map.call_args.kwargs["refresh_expiry"], False)

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

    def test_directory_location_filters_use_normalized_branch_locations(self):
        mumbai_user = User.objects.create_user(
            email="mumbai.branch@acuite.in",
            first_name="Mumbai",
            last_name="Branch",
            title="Analyst",
            department="Technology",
            location="Mumbai 603",
        )
        delhi_user = User.objects.create_user(
            email="delhi.branch@acuite.in",
            first_name="Delhi",
            last_name="Branch",
            title="Analyst",
            department="Technology",
            location="Delhi",
        )
        DirectoryProfile.objects.create(
            user=mumbai_user,
            company_name="Acuite",
            department_for_connect="Rating Operations",
            city="Mumbai",
            office_location="Mumbai 905",
        )
        DirectoryProfile.objects.create(
            user=delhi_user,
            company_name="Acuite",
            department_for_connect="Rating Operations",
            city="Delhi",
            office_location="Delhi",
        )

        response = self.client.get("/api/directory/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["filters"]["location"], ["Mumbai", "New Delhi"])
        mumbai_result = next(item for item in payload["results"] if item["email"] == "mumbai.branch@acuite.in")
        self.assertEqual(mumbai_result["branch_location"], "Mumbai")

    def test_directory_can_filter_by_normalized_branch_location(self):
        mumbai_a = User.objects.create_user(
            email="mumbai.603@acuite.in",
            first_name="Mumbai",
            last_name="603",
            title="Analyst",
            department="Technology",
            location="Mumbai 603",
        )
        mumbai_b = User.objects.create_user(
            email="mumbai.905@acuite.in",
            first_name="Mumbai",
            last_name="905",
            title="Analyst",
            department="Technology",
            location="Mumbai 905",
        )
        DirectoryProfile.objects.create(
            user=mumbai_a,
            company_name="Acuite",
            department_for_connect="Rating Operations",
            city="Mumbai",
            office_location="Mumbai 603",
        )
        DirectoryProfile.objects.create(
            user=mumbai_b,
            company_name="Acuite",
            department_for_connect="Rating Operations",
            city="Mumbai",
            office_location="Mumbai 905",
        )

        response = self.client.get("/api/directory/", {"location": "Mumbai"})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 2)

    def test_directory_branch_location_prefers_office_location_over_city(self):
        user = User.objects.create_user(
            email="wrong.city@acuite.in",
            first_name="Wrong",
            last_name="City",
            title="Analyst",
            department="Technology",
            location="Krishna",
        )
        DirectoryProfile.objects.create(
            user=user,
            company_name="Acuite",
            department_for_connect="Rating Operations",
            city="Krishna",
            office_location="Mumbai 905",
        )

        response = self.client.get("/api/directory/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("Mumbai", payload["filters"]["location"])
        self.assertNotIn("Krishna", payload["filters"]["location"])
        result = next(item for item in payload["results"] if item["email"] == "wrong.city@acuite.in")
        self.assertEqual(result["branch_location"], "Mumbai")

    def test_directory_locations_are_limited_to_official_offices(self):
        user = User.objects.create_user(
            email="stray.city@acuite.in",
            first_name="Stray",
            last_name="City",
            title="Analyst",
            department="Technology",
            location="West Delhi",
        )
        DirectoryProfile.objects.create(
            user=user,
            company_name="Acuite",
            department_for_connect="Rating Operations",
            city="Krishna",
            office_location="",
        )

        response = self.client.get("/api/directory/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertNotIn("Krishna", payload["filters"]["location"])
        self.assertNotIn("West Delhi", payload["filters"]["location"])
        result = next(item for item in payload["results"] if item["email"] == "stray.city@acuite.in")
        self.assertEqual(result["branch_location"], "")

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

    def test_authenticated_user_can_load_profile_builder_payload(self):
        user = User.objects.create_user(
            email="reshma.polasa@acuite.in",
            first_name="Reshma",
            last_name="Polasa",
            title="Head - Operations",
            department="Technology",
            location="Hyderabad",
        )
        DirectoryProfile.objects.create(
            user=user,
            company_name="Acuite",
            department_for_connect="Rating Operations",
            skills=["Python & SQL"],
            hobbies=["Reading"],
            interests=["Training"],
            profile_photos=["data:image/png;base64,AAAA"],
            city="Hyderabad",
            office_location="Hyderabad",
        )
        self.client.force_login(user)

        response = self.client.get("/api/directory/me/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["profile"]["email"], user.email)
        self.assertIn("Python & SQL", payload["profile"]["skills"])
        self.assertIn("MS Excel", payload["skill_library"])
        self.assertNotIn("Credit Analysis", payload["skill_library"])
        self.assertEqual(payload["limits"]["max_skills"], 3)
        self.assertEqual(payload["limits"]["max_hobbies"], 3)

    def test_authenticated_user_can_update_profile_builder_fields(self):
        user = User.objects.create_user(
            email="chitra.mohan@acuite.in",
            first_name="Chitra",
            last_name="Mohan",
            department="Compliance",
            location="Mumbai",
        )
        DirectoryProfile.objects.create(user=user, department_for_connect="Corporate")
        self.client.force_login(user)

        response = self.client.post(
            "/api/directory/me/",
            data={
                "skills": ["Leadership", "Public Speaking", "MS Excel", "Not In Library"],
                "hobbies": ["Reading Club", "Cricket Club", "Health Club", "Running"],
                "interests": "Training Delivery, CSR",
                "profile_photos": [
                    "data:image/png;base64,AAAA",
                    "data:image/jpeg;base64,BBBB",
                    "data:image/png;base64,CCCC",
                ],
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        user.directory_profile.refresh_from_db()
        self.assertEqual(user.directory_profile.skills, ["Leadership", "Public Speaking", "MS Excel"])
        self.assertEqual(user.directory_profile.hobbies, ["Reading Club", "Cricket Club", "Health Club"])
        self.assertEqual(user.directory_profile.interests, ["Training Delivery", "CSR"])
        self.assertEqual(len(user.directory_profile.profile_photos), 2)

# Create your tests here.
