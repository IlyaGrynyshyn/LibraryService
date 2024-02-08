from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/library/", include("books.urls"), name="books"),
    path("api/users/", include("users.urls"), name="users"),
    path("api/borrowsings/", include("borrowings.urls"), name="borrowings"),
    path("api/doc/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/doc/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
