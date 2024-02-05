from django.test import TestCase
from django.contrib.auth import get_user_model
from books.models import Book
from .models import Borrowing


class BorrowingModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@user.com", password="testpassword"
        )
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover=Book.CoverType.HARD,
            inventory=10,
            daily_fee="9.99",
        )

    def test_borrowing_model(self):
        borrowing = Borrowing.objects.create(
            borrow_date="2022-01-01",
            expected_return_date="2022-02-01",
            actual_return_date="2022-01-15",
            book_id=self.book,
            user=self.user,
        )

        self.assertEqual(str(borrowing), "2022-01-01 - test@user.com")

    def test_borrowing_model_fields(self):
        borrowing = Borrowing.objects.create(
            borrow_date="2022-01-01",
            expected_return_date="2022-02-01",
            actual_return_date="2022-01-15",
            book_id=self.book,
            user=self.user,
        )

        saved_borrowing = Borrowing.objects.get(pk=borrowing.id)
        self.assertEqual(str(saved_borrowing.borrow_date), "2022-01-01")
        self.assertEqual(str(saved_borrowing.expected_return_date), "2022-02-01")
        self.assertEqual(str(saved_borrowing.actual_return_date), "2022-01-15")
        self.assertEqual(saved_borrowing.book_id, self.book)
        self.assertEqual(saved_borrowing.user, self.user)
