from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingListSerializer


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
            book=self.book,
            user=self.user,
        )
        self.assertEqual(str(borrowing), f"{timezone.now().date()} - test@user.com")

    def test_borrowing_model_fields(self):
        borrowing = Borrowing.objects.create(
            borrow_date="2022-01-01",
            expected_return_date="2022-02-01",
            book=self.book,
            user=self.user,
        )

        saved_borrowing = Borrowing.objects.get(pk=borrowing.id)
        self.assertEqual(str(saved_borrowing.borrow_date), str(timezone.now().date()))
        self.assertEqual(str(saved_borrowing.expected_return_date), "2022-02-01")
        self.assertEqual(saved_borrowing.book, self.book)
        self.assertEqual(saved_borrowing.user, self.user)


class BorrowingViewTests(TestCase):
    BORROWING_URL = reverse("borrowings:borrowing-list")

    def setUp(self):
        self.client = APIClient()
        user = get_user_model()
        self.admin_user = user.objects.create_user(
            email="admin@example.com", password="adminpassword", is_staff=True
        )
        self.user = user.objects.create_user(
            email="user@example.com", password="userpass"
        )
        self.book = Book.objects.create(
            title="Sample Book",
            author="John Doe",
            cover=Book.CoverType.HARD,
            inventory=1,
            daily_fee="19.99",
        )
        self.borrowing = Borrowing.objects.create(
            borrow_date="2022-01-01",
            expected_return_date="2022-02-01",
            user=self.user,
            book=self.book,
        )

        self.admin_token = self.generate_jwt_token(self.admin_user)
        self.user_token = self.generate_jwt_token(self.user)

    def generate_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        access_token = AccessToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(access_token),
        }

    def test_admin_user_create_borrowing(self):
        self.client.credentials(HTTP_AUTHORIZE=f'Bearer {self.admin_token["access"]}')

        initial_inventory = self.book.inventory

        payload = {
            "borrow_date": "2024-02-06",
            "expected_return_date": "2024-02-10",
            "book": self.book.id,
        }

        response = self.client.post(self.BORROWING_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        borrowing = Borrowing.objects.get(id=response.data["id"])
        updated_book = Book.objects.get(id=self.book.id)

        self.assertEqual(borrowing.user, self.admin_user)
        self.assertEqual(updated_book.inventory, initial_inventory - 1)

    def test_create_borrowing_with_zero_inventory(self):
        self.client.credentials(HTTP_AUTHORIZE=f'Bearer {self.admin_token["access"]}')

        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="Hard",
            inventory=0,
            daily_fee=10.0,
        )

        payload = {
            "borrow_date": "2024-02-06",
            "expected_return_date": "2024-02-10",
            "book": book.id,
        }

        response = self.client.post(self.BORROWING_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Unfortunately, this book is out of stock.",
            response.data["non_field_errors"],
        )

    def test_retrieve_borrowing(self):
        self.client.credentials(HTTP_AUTHORIZE=f'Bearer {self.user_token["access"]}')
        borrowing = Borrowing.objects.create(
            borrow_date="2022-01-01",
            expected_return_date="2022-02-01",
            user=self.user,
            book=self.book,
        )

        response = self.client.get(
            reverse("borrowings:borrowing-detail", kwargs={"pk": borrowing.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_filter_is_active_true(self):
        self.client.credentials(HTTP_AUTHORIZE=f'Bearer {self.admin_token["access"]}')

        response = self.client.get(self.BORROWING_URL, {"is_active": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = BorrowingListSerializer(
            Borrowing.objects.filter(actual_return_date__isnull=True), many=True
        )
        self.assertEqual(response.data, serializer.data)

    def test_filter_is_active_false(self):
        self.client.credentials(HTTP_AUTHORIZE=f'Bearer {self.admin_token["access"]}')
        response = self.client.get(self.BORROWING_URL, {"is_active": "false"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = BorrowingListSerializer(
            Borrowing.objects.filter(actual_return_date__isnull=False), many=True
        )
        self.assertEqual(response.data, serializer.data)

    def test_filter_user_id_by_admin(self):
        self.client.credentials(HTTP_AUTHORIZE=f'Bearer {self.admin_token["access"]}')
        response = self.client.get(self.BORROWING_URL, {"user_id": self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = BorrowingListSerializer(
            Borrowing.objects.filter(user=self.user), many=True
        )
        self.assertEqual(response.data, serializer.data)

    def test_return_borrowing_success(self):
        self.client.credentials(HTTP_AUTHORIZE=f'Bearer {self.admin_token["access"]}')
        response = self.client.post(
            reverse("borrowings:borrowing-return", kwargs={"pk": self.borrowing.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.borrowing.refresh_from_db()
        self.assertNotEquals(self.borrowing.actual_return_date, None)
        self.assertEqual(self.borrowing.book.inventory, 2)
