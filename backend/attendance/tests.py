from django.test import TestCase, override_settings
from django.utils import timezone

from accounts.models import User
from directory.models import DirectoryProfile

from .models import AttendanceDayRecord


class AttendanceApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="employee@acuite.in",
            password="testpass123",
            first_name="Employee",
            last_name="One",
            employment_status=User.EmploymentStatus.ACTIVE,
            access_level=User.AccessLevel.EMPLOYEE,
            must_change_password=False,
            password_changed_at=timezone.now(),
        )
        DirectoryProfile.objects.create(user=self.user, office_location="Mumbai", is_visible=True)
        self.admin = User.objects.create_user(
            email="admin@acuite.in",
            password="testpass123",
            first_name="Admin",
            last_name="User",
            employment_status=User.EmploymentStatus.ACTIVE,
            access_level=User.AccessLevel.ADMIN,
            must_change_password=False,
            password_changed_at=timezone.now(),
        )
        DirectoryProfile.objects.create(user=self.admin, office_location="Mumbai", is_visible=True)

    @override_settings(ATTENDANCE_OFFICE_NETWORKS="")
    def test_status_is_not_marked_when_office_networks_are_not_configured(self):
        self.client.force_login(self.user)

        response = self.client.get("/api/attendance/status/", REMOTE_ADDR="10.10.1.7")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "not_marked")
        self.assertFalse(payload["office_network_configured"])
        self.assertFalse(AttendanceDayRecord.objects.filter(user=self.user).exists())

    @override_settings(ATTENDANCE_OFFICE_NETWORKS="Mumbai=10.10.0.0/16")
    def test_office_activity_records_punch_in_and_logout_confirms_punch_out(self):
        self.client.force_login(self.user)

        status_response = self.client.get("/api/attendance/status/", REMOTE_ADDR="10.10.1.7")

        self.assertEqual(status_response.status_code, 200)
        self.assertEqual(status_response.json()["status"], "no_punchout")
        record = AttendanceDayRecord.objects.get(user=self.user, attendance_date=timezone.localdate())
        self.assertEqual(record.office_label, "Mumbai")
        self.assertEqual(record.status, AttendanceDayRecord.Status.NO_PUNCHOUT)

        logout_response = self.client.post("/api/accounts/auth/logout/", REMOTE_ADDR="10.10.1.7")

        self.assertEqual(logout_response.status_code, 200)
        record.refresh_from_db()
        self.assertEqual(record.status, AttendanceDayRecord.Status.PRESENT)
        self.assertEqual(record.punch_out_source, AttendanceDayRecord.Source.LOGOUT)

    @override_settings(ATTENDANCE_OFFICE_NETWORKS="Mumbai=10.10.0.0/16")
    def test_non_connect_attendance_employee_is_not_applicable(self):
        profile = self.user.directory_profile
        profile.attendance_recording_method = "Field attendance"
        profile.save(update_fields=["attendance_recording_method", "updated_at"])
        self.client.force_login(self.user)

        response = self.client.get("/api/attendance/status/", REMOTE_ADDR="10.10.1.7")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "not_applicable")
        self.assertFalse(AttendanceDayRecord.objects.filter(user=self.user).exists())

    @override_settings(ATTENDANCE_OFFICE_NETWORKS="Mumbai=10.10.0.0/16")
    def test_admin_overview_returns_employee_attendance_statuses(self):
        self.client.force_login(self.admin)

        response = self.client.get("/api/attendance/admin/overview/", REMOTE_ADDR="10.10.1.7")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("results", payload)
        self.assertTrue(any(row["user"]["email"] == self.user.email for row in payload["results"]))
