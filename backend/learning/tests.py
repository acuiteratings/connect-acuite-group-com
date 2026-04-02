import json

from django.test import TestCase

from accounts.models import User

from .models import Book, BookRequisition


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

    def test_books_endpoint_lists_active_titles(self):
        response = self.client.get("/api/learning/books/")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertGreaterEqual(payload["count"], 1)
        self.assertTrue(
            any(item["title"] == "The Intelligent Investor" for item in payload["results"])
        )
        self.assertGreaterEqual(payload["summary"]["catalog_count"], 1)

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
