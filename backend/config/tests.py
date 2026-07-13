from django.test import TestCase

from accounts.models import User


class LoginPageRedirectTests(TestCase):
    def test_authenticated_employee_is_redirected_to_home_landing_override(self):
        user = User.objects.create_user(
            email="employee@acuite.in",
            password="TempPass@123",
            employment_status=User.EmploymentStatus.ACTIVE,
            access_level=User.AccessLevel.EMPLOYEE,
            is_active=True,
            must_change_password=False,
        )
        self.client.force_login(user)

        response = self.client.get("/login.html")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/?landing=home")

    def test_authenticated_admin_is_redirected_to_home_landing_override(self):
        user = User.objects.create_user(
            email="admin@acuite.in",
            password="TempPass@123",
            employment_status=User.EmploymentStatus.ACTIVE,
            access_level=User.AccessLevel.ADMIN,
            is_active=True,
            must_change_password=False,
        )
        self.client.force_login(user)

        response = self.client.get("/login.html")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/?landing=home")
