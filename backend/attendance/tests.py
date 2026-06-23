from datetime import date, datetime, timedelta
from unittest.mock import patch

from django.test import RequestFactory, TestCase, override_settings
from django.utils import timezone

from accounts.models import EmployeeSSOIdentitySnapshot, User
from directory.models import DirectoryProfile

from .models import AttendanceDayRecord
from .services import capture_attendance_activity, working_day_status


WORKING_DAY = date(2026, 5, 8)


class AttendanceApiTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
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
        EmployeeSSOIdentitySnapshot.objects.create(
            user=self.user,
            sso_user_id="sso-employee-1",
            email=self.user.email,
            full_name=self.user.full_name,
            employee_id="EMP9001",
        )
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

        with patch("attendance.services.timezone.localdate", return_value=WORKING_DAY):
            response = self.client.get("/api/attendance/status/", REMOTE_ADDR="10.10.1.7")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "not_marked")
        self.assertFalse(payload["office_network_configured"])
        self.assertFalse(AttendanceDayRecord.objects.filter(user=self.user).exists())

    @override_settings(ATTENDANCE_OFFICE_NETWORKS="Mumbai=10.10.0.0/16")
    def test_office_activity_records_punch_in_and_logout_confirms_punch_out(self):
        self.client.force_login(self.user)

        with patch("attendance.services.timezone.localdate", return_value=WORKING_DAY):
            status_response = self.client.get("/api/attendance/status/", REMOTE_ADDR="10.10.1.7")

        self.assertEqual(status_response.status_code, 200)
        self.assertEqual(status_response.json()["status"], "no_punchout")
        record = AttendanceDayRecord.objects.get(user=self.user, attendance_date=WORKING_DAY)
        self.assertEqual(record.office_label, "Mumbai")
        self.assertEqual(record.status, AttendanceDayRecord.Status.NO_PUNCHOUT)

        with patch("attendance.services.timezone.localdate", return_value=WORKING_DAY):
            logout_response = self.client.post("/api/accounts/auth/logout/", REMOTE_ADDR="10.10.1.7")

        self.assertEqual(logout_response.status_code, 200)
        record.refresh_from_db()
        self.assertEqual(record.status, AttendanceDayRecord.Status.PRESENT)
        self.assertEqual(record.punch_out_source, AttendanceDayRecord.Source.LOGOUT)

    def test_default_office_ip_allowlist_records_attendance(self):
        self.client.force_login(self.user)

        with patch("attendance.services.timezone.localdate", return_value=WORKING_DAY):
            response = self.client.get("/api/attendance/status/", REMOTE_ADDR="122.179.133.53")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "no_punchout")
        record = AttendanceDayRecord.objects.get(user=self.user, attendance_date=WORKING_DAY)
        self.assertEqual(record.punch_in_ip, "122.179.133.53")

    @override_settings(
        ATTENDANCE_OFFICE_NETWORKS="Mumbai=10.10.0.0/16",
        ATTENDANCE_ACTIVITY_WRITE_THROTTLE_SECONDS=300,
    )
    def test_repeated_activity_within_throttle_window_does_not_rewrite_attendance_record(self):
        request = self.factory.get("/api/attendance/status/", REMOTE_ADDR="10.10.1.7")
        request.user = self.user
        first_seen = timezone.make_aware(datetime(2026, 5, 8, 9, 30, 0))
        second_seen = first_seen + timedelta(seconds=90)

        with patch("attendance.services.timezone.localdate", return_value=WORKING_DAY):
            with patch("attendance.services.timezone.now", return_value=first_seen):
                first_record = capture_attendance_activity(request)
            with patch("attendance.services.timezone.now", return_value=second_seen):
                second_record = capture_attendance_activity(request)

        self.assertIsNotNone(first_record)
        self.assertIsNotNone(second_record)
        record = AttendanceDayRecord.objects.get(user=self.user, attendance_date=WORKING_DAY)
        self.assertEqual(record.first_activity_at, first_seen)
        self.assertEqual(record.last_activity_at, first_seen)
        self.assertEqual(record.punch_out_at, first_seen)

    @override_settings(
        ATTENDANCE_OFFICE_NETWORKS="Mumbai=10.10.0.0/16",
        ATTENDANCE_ACTIVITY_WRITE_THROTTLE_SECONDS=300,
    )
    def test_activity_after_throttle_window_refreshes_attendance_record(self):
        request = self.factory.get("/api/attendance/status/", REMOTE_ADDR="10.10.1.7")
        request.user = self.user
        first_seen = timezone.make_aware(datetime(2026, 5, 8, 9, 30, 0))
        second_seen = first_seen + timedelta(minutes=6)

        with patch("attendance.services.timezone.localdate", return_value=WORKING_DAY):
            with patch("attendance.services.timezone.now", return_value=first_seen):
                capture_attendance_activity(request)
            with patch("attendance.services.timezone.now", return_value=second_seen):
                capture_attendance_activity(request)

        record = AttendanceDayRecord.objects.get(user=self.user, attendance_date=WORKING_DAY)
        self.assertEqual(record.first_activity_at, first_seen)
        self.assertEqual(record.last_activity_at, second_seen)
        self.assertEqual(record.punch_out_at, second_seen)

    @override_settings(ATTENDANCE_OFFICE_NETWORKS="Mumbai=10.10.0.0/16")
    def test_non_connect_attendance_employee_is_not_applicable(self):
        profile = self.user.directory_profile
        profile.attendance_recording_method = "Field attendance"
        profile.save(update_fields=["attendance_recording_method", "updated_at"])
        self.client.force_login(self.user)

        with patch("attendance.services.timezone.localdate", return_value=WORKING_DAY):
            response = self.client.get("/api/attendance/status/", REMOTE_ADDR="10.10.1.7")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "not_applicable")
        self.assertFalse(AttendanceDayRecord.objects.filter(user=self.user).exists())

    def test_branch_specific_holiday_status_uses_employee_location(self):
        mumbai_status, mumbai_label = working_day_status(date(2026, 4, 3), self.user.directory_profile)
        self.assertEqual(mumbai_status, AttendanceDayRecord.Status.HOLIDAY)
        self.assertEqual(mumbai_label, "Good Friday")

        self.user.directory_profile.office_location = "Delhi"
        self.user.directory_profile.save(update_fields=["office_location", "updated_at"])
        delhi_status, delhi_label = working_day_status(date(2026, 4, 3), self.user.directory_profile)
        self.assertIsNone(delhi_status)
        self.assertEqual(delhi_label, "")

        unknown_status, unknown_label = working_day_status(date(2026, 4, 3), None)
        self.assertIsNone(unknown_status)
        self.assertEqual(unknown_label, "")

    @override_settings(CONNECT_ATTENDANCE_EXPORT_TOKENS=["export-token"])
    def test_holiday_export_returns_branch_wise_records(self):
        denied = self.client.get("/api/attendance/export/holidays/?year=2026")
        self.assertEqual(denied.status_code, 401)

        response = self.client.get(
            "/api/attendance/export/holidays/?year=2026",
            HTTP_AUTHORIZATION="Bearer export-token",
        )
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 22)
        pongal = next(item for item in payload["holidays"] if item["name"] == "Pongal")
        self.assertEqual(pongal["applicable_locations"], ["Chennai", "Hyderabad"])
        self.assertFalse(pongal["applies_to_all_offices"])
        self.assertEqual(pongal["category"], "Festive")
        self.assertEqual(pongal["state_holiday"], "Tamil Nadu, Telangana")

        delhi_response = self.client.get(
            "/api/attendance/export/holidays/?year=2026&location=Delhi",
            HTTP_AUTHORIZATION="Bearer export-token",
        )
        self.assertEqual(delhi_response.status_code, 200)
        delhi_holidays = {item["name"] for item in delhi_response.json()["holidays"]}
        self.assertIn("Janmashtami", delhi_holidays)
        self.assertIn("Republic Day", delhi_holidays)
        self.assertNotIn("Good Friday", delhi_holidays)

    @override_settings(ATTENDANCE_OFFICE_NETWORKS="Mumbai=10.10.0.0/16")
    def test_admin_overview_returns_employee_attendance_statuses(self):
        self.client.force_login(self.admin)

        with patch("attendance.services.timezone.localdate", return_value=WORKING_DAY):
            response = self.client.get("/api/attendance/admin/overview/", REMOTE_ADDR="10.10.1.7")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("results", payload)
        self.assertTrue(any(row["user"]["email"] == self.user.email for row in payload["results"]))

    @override_settings(
        ATTENDANCE_OFFICE_NETWORKS="Mumbai=10.10.0.0/16",
        CONNECT_ATTENDANCE_EXPORT_TOKENS=["export-token"],
    )
    def test_export_requires_service_token_and_returns_raw_attendance_rows(self):
        today = WORKING_DAY
        AttendanceDayRecord.objects.create(
            user=self.user,
            attendance_date=today,
            status=AttendanceDayRecord.Status.NO_PUNCHOUT,
            punch_in_at=timezone.now(),
            office_label="Mumbai",
            punch_in_source=AttendanceDayRecord.Source.ACTIVITY,
            requires_regularization=True,
        )

        denied = self.client.get(
            f"/api/attendance/export/?from={today.isoformat()}&to={today.isoformat()}"
        )
        self.assertEqual(denied.status_code, 401)

        response = self.client.get(
            f"/api/attendance/export/?from={today.isoformat()}&to={today.isoformat()}",
            HTTP_AUTHORIZATION="Bearer export-token",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        row = next(item for item in payload["records"] if item["email"] == self.user.email)
        self.assertEqual(row["employee_sso_id"], "sso-employee-1")
        self.assertEqual(row["employee_code"], "EMP9001")
        self.assertEqual(row["status"], "no_punchout")
        self.assertTrue(row["requires_regularization"])

    @override_settings(
        ATTENDANCE_OFFICE_NETWORKS="Mumbai=10.10.0.0/16",
        CONNECT_ATTENDANCE_EXPORT_TOKENS=["export-token"],
    )
    def test_employee_day_export_returns_only_requested_employee_day(self):
        today = WORKING_DAY
        other_user = User.objects.create_user(
            email="other@acuite.in",
            password="testpass123",
            first_name="Other",
            last_name="Employee",
            employment_status=User.EmploymentStatus.ACTIVE,
            access_level=User.AccessLevel.EMPLOYEE,
            must_change_password=False,
            password_changed_at=timezone.now(),
        )
        DirectoryProfile.objects.create(user=other_user, office_location="Mumbai", is_visible=True)
        AttendanceDayRecord.objects.create(
            user=self.user,
            attendance_date=today,
            status=AttendanceDayRecord.Status.NO_PUNCHOUT,
            punch_in_at=timezone.now(),
            office_label="Mumbai",
            punch_in_source=AttendanceDayRecord.Source.ACTIVITY,
            requires_regularization=True,
        )
        AttendanceDayRecord.objects.create(
            user=other_user,
            attendance_date=today,
            status=AttendanceDayRecord.Status.PRESENT,
            punch_in_at=timezone.now(),
            punch_out_at=timezone.now(),
            office_label="Mumbai",
            punch_in_source=AttendanceDayRecord.Source.ACTIVITY,
            punch_out_source=AttendanceDayRecord.Source.LOGOUT,
        )

        denied = self.client.get(
            f"/api/attendance/export/employee-day/?date={today.isoformat()}&employee_sso_id=sso-employee-1"
        )
        self.assertEqual(denied.status_code, 401)

        response = self.client.get(
            f"/api/attendance/export/employee-day/?date={today.isoformat()}&employee_sso_id=sso-employee-1",
            HTTP_AUTHORIZATION="Bearer export-token",
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["date"], today.isoformat())
        self.assertEqual(len(payload["records"]), 1)
        self.assertEqual(payload["records"][0]["email"], self.user.email)
        self.assertEqual(payload["records"][0]["status"], "no_punchout")
