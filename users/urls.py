from django.urls import path

from users.views import CreateUserView, ManageUserView
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path("me/", ManageUserView.as_view(), name="me"),
    path(
        "token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
]

app_name = "users"
