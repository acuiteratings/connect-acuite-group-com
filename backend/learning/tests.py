import json

from django.test import TestCase

from accounts.models import User

from .models import Book, BookLike, BookRequisition


class LearningApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="book.reader@acuite.in",
            password="testpass123",
            first_name="Book",
            last_name="Reader",
        )
        self.book = Book.objects.create(
            title="The Intelligent Investor",
            author="Benjamin Graham",
            total_copies=2,
            summary="A classic on investing discipline.",
        )
        self.admin_user = User.objects.create_user(
            email="admin.library@acuite.in",
            password="testpass123",
            first_name="Admin",
            last_name="Library",
            is_staff=True,
        )

    def test_books_endpoint_lists_active_titles(self):
        response = self.client.get("/api/learning/books/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertGreaterEqual(payload["count"], 1)
        self.assertTrue(
            any(item["title"] == "The Intelligent Investor" for item in payload["results"])
        )
        self.assertGreaterEqual(payload["summary"]["catalog_count"], 1)
        title = next(item for item in payload["results"] if item["title"] == "The Intelligent Investor")
        self.assertEqual(title["like_count"], 0)
        self.assertFalse(title["current_user_has_liked"])

    def test_authenticated_employee_can_requisition_book(self):
        self.client.force_login(self.user)

        response = self.client.post(
            "/api/learning/requisitions/",
            data=json.dumps({"book_id": self.book.id, "note": "Would love this for the next discussion."}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        payload = response.json()
        self.assertEqual(payload["requisition"]["book"]["title"], "The Intelligent Investor")
        self.assertEqual(BookRequisition.objects.count(), 1)

    def test_employee_cannot_create_duplicate_open_requisition(self):
        BookRequisition.objects.create(book=self.book, requester=self.user)
        self.client.force_login(self.user)

        response = self.client.post(
            "/api/learning/requisitions/",
            data=json.dumps({"book_id": self.book.id}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("open request", response.json()["detail"])

    def test_admin_can_add_book(self):
        self.client.force_login(self.admin_user)

        response = self.client.post(
            "/api/learning/books/",
            data=json.dumps(
                {
                    "catalog_number": "999",
                    "title": "The Outsiders",
                    "author": "William Thorndike",
                    "category": "Leadership & Management",
                    "office_location": "Mumbai-Kanjurmarg",
                    "shelf_area": "CEO Cabin",
                    "shelf_label": "White Book Shelf",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["book"]["title"], "The Outsiders")

    def test_admin_can_approve_book_requisition(self):
        requisition = BookRequisition.objects.create(book=self.book, requester=self.user)
        self.client.force_login(self.admin_user)

        response = self.client.patch(
            f"/api/learning/requisitions/{requisition.id}/",
            data=json.dumps({"status": "approved"}),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        requisition.refresh_from_db()
        self.assertEqual(requisition.status, BookRequisition.Status.APPROVED)

    def test_authenticated_employee_can_toggle_book_like(self):
        self.client.force_login(self.user)

        first_response = self.client.post(f"/api/learning/books/{self.book.id}/likes/toggle/")

        self.assertEqual(first_response.status_code, 200)
        self.assertTrue(first_response.json()["liked"])
        self.assertEqual(first_response.json()["book"]["like_count"], 1)
        self.assertTrue(first_response.json()["book"]["current_user_has_liked"])
        self.assertEqual(BookLike.objects.count(), 1)

        second_response = self.client.post(f"/api/learning/books/{self.book.id}/likes/toggle/")

        self.assertEqual(second_response.status_code, 200)
        self.assertFalse(second_response.json()["liked"])
        self.assertEqual(second_response.json()["book"]["like_count"], 0)
        self.assertFalse(second_response.json()["book"]["current_user_has_liked"])
        self.assertEqual(BookLike.objects.count(), 0)
