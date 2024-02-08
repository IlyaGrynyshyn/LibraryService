from rest_framework import routers

from borrowings.views import BorrowingListView

router = routers.DefaultRouter()
router.register("", BorrowingListView, basename="borrowing")
urlpatterns = router.urls

app_name = "borrowings"
