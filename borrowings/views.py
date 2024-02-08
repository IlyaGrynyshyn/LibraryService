from django.db import transaction
from django.utils import timezone
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.permissions import IsAdminUserOrReadAndCreateOnly
from borrowings.serializers import (
    BorrowingDetailSerializer,
    BorrowingListSerializer,
)


class BorrowingListView(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    permission_classes = [IsAdminUserOrReadAndCreateOnly]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        return BorrowingListSerializer

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        is_active = self.request.query_params.get("is_active")
        user_id = self.request.query_params.get("user_id")
        queryset = Borrowing.objects.all()

        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)

        if user_id:
            users_ids = self._params_to_ints(user_id)
            queryset = queryset.filter(user_id__in=users_ids)

        if is_active:
            is_active = is_active.lower() == "true"
            queryset = queryset.filter(actual_return_date__isnull=is_active)

        return queryset

    def perform_create(self, serializer):
        updated_borrowing = serializer.save(user=self.request.user)
        updated_borrowing.book.inventory -= 1
        updated_borrowing.book.save()

    @action(
        detail=True,
        methods=["POST"],
        url_path="return",
        permission_classes=[permissions.IsAdminUser],
        url_name="return",
    )
    @transaction.atomic
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        if borrowing.actual_return_date:
            return Response(
                {"error": "Item has already been returned"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        borrowing.actual_return_date = timezone.now().date()
        borrowing.book.inventory += 1
        borrowing.book.save()
        borrowing.save()
        serializer = self.get_serializer(borrowing)
        return Response(serializer.data)
