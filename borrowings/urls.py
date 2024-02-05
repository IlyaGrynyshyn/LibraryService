from rest_framework import routers

from borrowings.views import BorrowingListView

router = routers.DefaultRouter()
router.register("", BorrowingListView)
urlpatterns = router.urls

app_name = "borrowings"
