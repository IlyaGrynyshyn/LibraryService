from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/library/", include("books.urls"), name="books"),
    path("api/users/", include("users.urls"), name="users"),
    path("api/borrowsings/", include("borrowings.urls"), name="borrowings"),
]
