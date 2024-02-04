from django.test import TestCase
from books.models import Book


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
