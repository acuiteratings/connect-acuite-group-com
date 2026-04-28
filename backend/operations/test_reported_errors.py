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

        reported_error_id = payload["results"][0]["id"]
        resolve_response = self.client.patch(
            f"/api/ops/reported-errors/admin/{reported_error_id}/resolve/",
            data=json.dumps({"is_resolved": True}),
            content_type="application/json",
        )
        self.assertEqual(resolve_response.status_code, 200)
        resolved_payload = resolve_response.json()["reported_error"]
        self.assertTrue(resolved_payload["is_resolved"])
        self.assertEqual(resolved_payload["resolved_by_email"], self.admin.email)

        reported_error = ReportedError.objects.get(pk=reported_error_id)
        self.assertTrue(reported_error.is_resolved)
        self.assertEqual(reported_error.resolved_by, self.admin)
        self.assertIsNotNone(reported_error.resolved_at)
        self.assertEqual(AuditLog.objects.filter(action="error.report.resolved").count(), 1)
