from rest_framework import serializers

from books.models import Book
from borrowings.models import Borrowing


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "is_active",
        )

    def create(self, validated_data):
        return Borrowing.objects.create(**validated_data)

    def validate(self, data):
        book = data["book"]
        if book and book.inventory == 0:
            raise serializers.ValidationError(
                "Unfortunately, this book is out of stock."
            )
        return data


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(read_only=True)
