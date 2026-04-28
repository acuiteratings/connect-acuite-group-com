from django.test import TestCase

from directory.models import DirectoryProfile

from .models import User


class EmployeeApiAccessMiddlewareTests(TestCase):
    def test_internal_api_requires_authenticated_employee(self):
        response = self.client.get("/api/directory/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(response.json()["detail"], "Authentication required.")

    def test_healthcheck_remains_public(self):
        response = self.client.get("/api/ops/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")

    def test_current_session_endpoint_remains_public(self):
        response = self.client.get("/api/accounts/me/")

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["authenticated"])

    def test_authenticated_employee_can_access_internal_api(self):
        user = User.objects.create_user(
            email="employee.api@acuite.in",
            first_name="Employee",
            last_name="Api",
        )
        DirectoryProfile.objects.create(user=user, department_for_connect="Corporate")
        self.client.force_login(user)

        response = self.client.get("/api/directory/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["count"], 1)
