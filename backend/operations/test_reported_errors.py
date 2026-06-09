import json

from django.test import TestCase

from accounts.models import User

from .models import AuditLog, ReportedError


class ReportedErrorAdminInboxTests(TestCase):
    def setUp(self):
        self.employee = User.objects.create_user(
            email="employee@acuite.in",
            password="testpass123",
            first_name="Employee",
            last_name="User",
            employment_status=User.EmploymentStatus.ACTIVE,
        )
        self.staff = User.objects.create_user(
            email="moderator@acuite.in",
            password="testpass123",
            first_name="Moderator",
            last_name="User",
            access_level=User.AccessLevel.MODERATOR,
            employment_status=User.EmploymentStatus.ACTIVE,
        )
        self.admin = User.objects.create_user(
            email="admin@acuite.in",
            password="testpass123",
            first_name="Admin",
            last_name="User",
            access_level=User.AccessLevel.ADMIN,
            employment_status=User.EmploymentStatus.ACTIVE,
        )

    def test_only_admin_can_list_all_and_resolve_reported_errors(self):
        ReportedError.objects.bulk_create(
            [
                ReportedError(
                    reporter=self.employee,
                    title=f"Reported issue {index}",
                    details="Something went wrong.",
                    source_tab="report-error",
                    attachment_name="error.png",
                    attachment_content_type="image/png",
                    attachment_size=12,
                    attachment_data_url="data:image/png;base64,ZXJyb3ItaW1hZ2U=",
                )
                for index in range(101)
            ]
        )

        self.client.force_login(self.employee)
        employee_response = self.client.get("/api/ops/reported-errors/admin/")
        self.assertEqual(employee_response.status_code, 403)

        self.client.force_login(self.staff)
        staff_response = self.client.get("/api/ops/reported-errors/admin/")
        self.assertEqual(staff_response.status_code, 403)

        self.client.force_login(self.admin)
        admin_response = self.client.get("/api/ops/reported-errors/admin/")
        self.assertEqual(admin_response.status_code, 200)
        payload = admin_response.json()
        self.assertEqual(payload["count"], 101)
        self.assertFalse(payload["results"][0]["is_resolved"])
        self.assertEqual(payload["results"][0]["attachment"]["name"], "error.png")

        reported_error_id = payload["results"][0]["id"]
        resolve_response = self.client.patch(
            f"/api/ops/reported-errors/admin/{reported_error_id}/resolve/",
            data=json.dumps({"resolution_outcome": "not_an_error", "resolution_comment": "This was expected behavior."}),
            content_type="application/json",
        )
        self.assertEqual(resolve_response.status_code, 200)
        resolved_payload = resolve_response.json()["reported_error"]
        self.assertTrue(resolved_payload["is_resolved"])
        self.assertEqual(resolved_payload["resolution_outcome"], "not_an_error")
        self.assertEqual(resolved_payload["resolution_comment"], "This was expected behavior.")
        self.assertEqual(resolved_payload["resolved_by_email"], self.admin.email)
        self.assertIsNone(resolved_payload["attachment"])

        reported_error = ReportedError.objects.get(pk=reported_error_id)
        self.assertTrue(reported_error.is_resolved)
        self.assertEqual(reported_error.resolution_outcome, ReportedError.ResolutionOutcome.NOT_AN_ERROR)
        self.assertEqual(reported_error.resolution_comment, "This was expected behavior.")
        self.assertEqual(reported_error.resolved_by, self.admin)
        self.assertIsNotNone(reported_error.resolved_at)
        self.assertEqual(reported_error.attachment_name, "")
        self.assertEqual(reported_error.attachment_content_type, "")
        self.assertEqual(reported_error.attachment_size, 0)
        self.assertEqual(reported_error.attachment_data_url, "")
        self.assertEqual(AuditLog.objects.filter(action="error.report.resolved").count(), 1)

    def test_reporter_sees_resolution_notification_once(self):
        reported_error = ReportedError.objects.create(
            reporter=self.employee,
            title="Directory issue",
            details="The location filter was wrong.",
            source_tab="directory",
            is_resolved=True,
            resolution_outcome=ReportedError.ResolutionOutcome.RESOLVED,
            resolution_comment="The location filter has been corrected.",
            resolved_by=self.admin,
        )

        self.client.force_login(self.employee)
        notification_response = self.client.get("/api/ops/reported-errors/notifications/")

        self.assertEqual(notification_response.status_code, 200)
        payload = notification_response.json()
        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["results"][0]["id"], reported_error.id)
        self.assertEqual(payload["results"][0]["resolution_comment"], "The location filter has been corrected.")

        acknowledge_response = self.client.patch(
            f"/api/ops/reported-errors/notifications/{reported_error.id}/acknowledge/"
        )
        self.assertEqual(acknowledge_response.status_code, 200)
        reported_error.refresh_from_db()
        self.assertIsNotNone(reported_error.reporter_seen_at)

        second_response = self.client.get("/api/ops/reported-errors/notifications/")
        self.assertEqual(second_response.json()["count"], 0)
