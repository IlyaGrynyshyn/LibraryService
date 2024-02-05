from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from books.models import Book
from django.urls import reverse


class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Sample Book",
            author="John Doe",
            cover=Book.CoverType.HARD,
            inventory=50,
            daily_fee=19.99,
        )

    def test_book_str_representation(self):
        self.assertEqual(str(self.book), "Sample Book by John Doe")

    def test_book_fields(self):
        saved_book = Book.objects.get(pk=self.book.id)
        self.assertEqual(saved_book.title, "Sample Book")
        self.assertEqual(saved_book.author, "John Doe")
        self.assertEqual(saved_book.cover, Book.CoverType.HARD)
        self.assertEqual(saved_book.inventory, 50)
        self.assertEqual(float(saved_book.daily_fee), 19.99)


class BookViewTest(APITestCase):
    BOOK_URL = reverse("books:book-list")

    def setUp(self):
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
            inventory=50,
            daily_fee="19.99",
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

    def test_list_books_permissions(self):
        # All users (authenticated or not) should be able to list books
        response = self.client.get(self.BOOK_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_list_books_permissions(self):
        response = self.client.get(self.BOOK_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_regular_user_create_book_permissions(self):
        self.client.credentials(
            HTTP_AUTHORIZE=f'Bearer {self.user_token["access"]}'
        )
        response = self.client.post(
            self.BOOK_URL,
            {
                "title": "New Book",
                "author": "Jane Doe",
                "cover": "Hard",
                "inventory": 30,
                "daily_fee": "15.99",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_create_book_permissions(self):
        self.client.credentials(
            HTTP_AUTHORIZE=f'Bearer {self.admin_token["access"]}'
        )

        response = self.client.post(
            self.BOOK_URL,
            {
                "title": "New Book",
                "author": "Jane Doe",
                "cover": "Hard",
                "inventory": 30,
                "daily_fee": "15.99",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_regular_user_update_book_permissions(self):
        self.client.credentials(
            HTTP_AUTHORIZE=f'Bearer {self.user_token["access"]}'
        )
        response = self.client.put(
            reverse("books:book-detail", kwargs={"pk": self.book.id}),
            {
                "title": "Updated Book",
                "author": "Jane Doe",
                "cover": "Hard",
                "inventory": 30,
                "daily_fee": "15.99",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_update_book_permissions(self):
        self.client.credentials(
            HTTP_AUTHORIZE=f'Bearer {self.admin_token["access"]}'
        )
        response = self.client.put(
            reverse("books:book-detail", kwargs={"pk": self.book.id}),
            {
                "title": "Updated Book",
                "author": "Doe",
                "cover": "Hard",
                "inventory": 30,
                "daily_fee": "11.99",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_delete_book_permissions(self):
        self.client.credentials(
            HTTP_AUTHORIZE=f'Bearer {self.admin_token["access"]}'
        )
        response = self.client.delete(
            reverse("books:book-detail", kwargs={"pk": self.book.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_regular_user_delete_book_permissions(self):
        self.client.credentials(
            HTTP_AUTHORIZE=f'Bearer {self.user_token["access"]}'
        )
        response = self.client.delete(
            reverse("books:book-detail", kwargs={"pk": self.book.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
