from datetime import date, datetime, timezone as dt_timezone

from django.test import TestCase
from django.utils import timezone

from accounts.models import User
from directory.models import DirectoryProfile

from .models import PeopleSyncFailure, PeopleSyncRun
from .services import run_people_sync


class PeopleSyncServiceTests(TestCase):
    def test_incremental_sync_creates_pending_user_and_directory_profile(self):
        def fake_fetch_page(*, updated_since=None, cursor=None):
            self.assertIsNone(updated_since)
            self.assertIsNone(cursor)
            return {
                "generated_at": "2026-04-04T12:00:00Z",
                "next_cursor": None,
                "employees": [
                    {
                        "employee_id": "ARR-00421",
                        "email": "nidhi.shree@acuite.in",
                        "first_name": "Nidhi",
                        "last_name": "Shree",
                        "display_name": "Nidhi Shree",
                        "full_name": "Nidhi Shree",
                        "title": "Associate",
                        "department": "Corporate Sector Ratings",
                        "function_name": "Business Development",
                        "company_name": "Acuité Ratings & Research Limited",
                        "office_location": "Mumbai",
                        "city": "Mumbai",
                        "mobile_number": "+91-9000000000",
                        "date_of_birth": "1994-04-04",
                        "joined_on": "2022-04-04",
                        "manager_employee_id": "",
                        "employment_status": "active",
                        "is_directory_visible": True,
                        "source_updated_at": "2026-04-04T11:58:23Z",
                    }
                ],
            }

        run = run_people_sync(fetch_page=fake_fetch_page)

        self.assertEqual(run.status, PeopleSyncRun.Status.SUCCESS)
        self.assertEqual(run.records_seen, 1)
        self.assertEqual(run.records_created, 1)
        user = User.objects.get(email="nidhi.shree@acuite.in")
        self.assertEqual(user.employee_code, "ARR-00421")
        self.assertEqual(user.employment_status, User.EmploymentStatus.PENDING)
        self.assertFalse(user.can_post_in_connect)
        self.assertTrue(user.is_directory_visible)
        profile = user.directory_profile
        self.assertEqual(profile.company_name, "Acuité Ratings & Research Limited")
        self.assertEqual(profile.function_name, "Business Development")
        self.assertEqual(profile.department_for_connect, "Business Development")
        self.assertEqual(profile.city, "Mumbai")

    def test_sync_updates_existing_user_and_links_manager(self):
        manager = User.objects.create_user(
            email="manager@acuite.in",
            employee_code="ARR-00012",
            first_name="Asha",
            last_name="Rao",
            employment_status=User.EmploymentStatus.ACTIVE,
            must_change_password=False,
        )
        user = User.objects.create_user(
            email="nidhi.shree@acuite.in",
            employee_code="ARR-00421",
            first_name="Nidhi",
            last_name="Shree",
            display_name="Nidhi Shree",
            title="Analyst",
            department="Sales",
            location="Kolkata",
            employment_status=User.EmploymentStatus.ACTIVE,
            must_change_password=False,
        )
        DirectoryProfile.objects.create(user=user, city="Kolkata", office_location="Kolkata")

        def fake_fetch_page(*, updated_since=None, cursor=None):
            return {
                "generated_at": "2026-04-04T12:00:00Z",
                "next_cursor": None,
                "employees": [
                    {
                        "employee_id": "ARR-00421",
                        "email": "nidhi.shree@acuite.in",
                        "full_name": "Nidhi Shree",
                        "title": "Associate",
                        "department": "Corporate Sector Ratings",
                        "function_name": "Business Development",
                        "company_name": "Acuite",
                        "office_location": "Mumbai",
                        "city": "Mumbai",
                        "mobile_number": "+91-9000000000",
                        "date_of_birth": "1994-04-04",
                        "joined_on": "2022-04-04",
                        "manager_employee_id": "ARR-00012",
                        "employment_status": "active",
                        "is_directory_visible": True,
                        "source_updated_at": "2026-04-04T11:58:23Z",
                    }
                ],
            }

        run = run_people_sync(fetch_page=fake_fetch_page)

        self.assertEqual(run.status, PeopleSyncRun.Status.SUCCESS)
        user.refresh_from_db()
        self.assertEqual(user.title, "Associate")
        self.assertEqual(user.department, "Corporate Sector Ratings")
        self.assertEqual(user.location, "Mumbai")
        profile = user.directory_profile
        self.assertEqual(profile.manager_id, manager.id)
        self.assertEqual(profile.department_for_connect, "Business Development")
        self.assertEqual(profile.date_of_birth, date(1994, 4, 4))
        self.assertEqual(profile.joined_on, date(2022, 4, 4))

    def test_sync_keeps_existing_celebration_dates_when_source_values_are_blank(self):
        user = User.objects.create_user(
            email="nidhi.shree@acuite.in",
            employee_code="ARR-00421",
            first_name="Nidhi",
            last_name="Shree",
            display_name="Nidhi Shree",
            employment_status=User.EmploymentStatus.ACTIVE,
            must_change_password=False,
        )
        DirectoryProfile.objects.create(
            user=user,
            city="Mumbai",
            office_location="Mumbai",
            date_of_birth=date(1994, 4, 4),
            joined_on=date(2022, 4, 4),
        )

        def fake_fetch_page(*, updated_since=None, cursor=None):
            return {
                "generated_at": "2026-04-04T12:00:00Z",
                "next_cursor": None,
                "employees": [
                    {
                        "employee_id": "ARR-00421",
                        "email": "nidhi.shree@acuite.in",
                        "full_name": "Nidhi Shree",
                        "title": "Associate",
                        "department": "Corporate Sector Ratings",
                        "function_name": "Business Development",
                        "company_name": "Acuite",
                        "office_location": "Mumbai",
                        "city": "Mumbai",
                        "mobile_number": "+91-9000000000",
                        "date_of_birth": "",
                        "joined_on": "",
                        "manager_employee_id": "",
                        "employment_status": "active",
                        "is_directory_visible": True,
                        "source_updated_at": "2026-04-04T11:58:23Z",
                    }
                ],
            }

        run_people_sync(fetch_page=fake_fetch_page)

        profile = DirectoryProfile.objects.get(user=user)
        self.assertEqual(profile.date_of_birth, date(1994, 4, 4))
        self.assertEqual(profile.joined_on, date(2022, 4, 4))

    def test_partial_success_logs_failures_and_keeps_same_checkpoint(self):
        checkpoint = timezone.make_aware(datetime(2026, 4, 4, 10, 0, 0), dt_timezone.utc)

        def fake_fetch_page(*, updated_since=None, cursor=None):
            self.assertEqual(updated_since, checkpoint)
            return {
                "generated_at": "2026-04-04T12:00:00Z",
                "next_cursor": None,
                "employees": [
                    {
                        "employee_id": "ARR-00421",
                        "email": "nidhi.shree@acuite.in",
                        "full_name": "Nidhi Shree",
                        "employment_status": "active",
                        "is_directory_visible": True,
                        "source_updated_at": "2026-04-04T11:58:23Z",
                    },
                    {
                        "employee_id": "",
                        "email": "broken@acuite.in",
                        "full_name": "Broken Record",
                        "employment_status": "active",
                        "is_directory_visible": True,
                        "source_updated_at": "2026-04-04T11:59:23Z",
                    },
                ],
            }

        run = run_people_sync(requested_updated_since=checkpoint, fetch_page=fake_fetch_page)

        self.assertEqual(run.status, PeopleSyncRun.Status.PARTIAL_SUCCESS)
        self.assertEqual(run.records_seen, 2)
        self.assertEqual(run.records_failed, 1)
        self.assertEqual(run.next_updated_since, checkpoint)
        self.assertEqual(PeopleSyncFailure.objects.count(), 1)

    def test_incremental_sync_uses_latest_success_checkpoint(self):
        checkpoint = timezone.make_aware(datetime(2026, 4, 4, 9, 0, 0), dt_timezone.utc)
        PeopleSyncRun.objects.create(
            sync_type=PeopleSyncRun.SyncType.INCREMENTAL,
            status=PeopleSyncRun.Status.SUCCESS,
            started_at=timezone.now(),
            finished_at=timezone.now(),
            next_updated_since=checkpoint,
        )
        seen = {}

        def fake_fetch_page(*, updated_since=None, cursor=None):
            seen["updated_since"] = updated_since
            return {
                "generated_at": "2026-04-04T12:00:00Z",
                "next_cursor": None,
                "employees": [],
            }

        run_people_sync(fetch_page=fake_fetch_page)

        self.assertEqual(seen["updated_since"], checkpoint)
