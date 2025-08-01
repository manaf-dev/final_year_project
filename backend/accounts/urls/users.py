from django.urls import path, include
from accounts.views.users import PasswordViewSet
from accounts.views.users import UserAccountViewSet, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

USERS_URLS = [
    path("auth/login/", LoginView.as_view()),
    path("auth/registration/", UserAccountViewSet.as_view({"post": "register_intern"})),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", UserAccountViewSet.as_view({"get": "list"})),
    path("users/supervisors/", UserAccountViewSet.as_view({"get": "list_supervisors"})),
    path("user/<str:user_id>/info/", UserAccountViewSet.as_view({"get": "retrieve"})),
    path("user/<str:user_id>/update/", UserAccountViewSet.as_view({"put": "update"})),
    path(
        "user/<str:user_id>/delete/", UserAccountViewSet.as_view({"delete": "destroy"})
    ),
    path(
        "cohort/<str:year>/interns/",
        UserAccountViewSet.as_view({"get": "get_cohort_interns"}),
    ),
    path(
        "password/reset/",
        PasswordViewSet.as_view({"post": "request_token"}),
    ),
    path(
        "password/reset/confirm/<str:token>/",
        PasswordViewSet.as_view({"post": "reset_password"}),
    ),
    path(
        "auth/password/change/",
        PasswordViewSet.as_view({"put": "change_password"}),
    ),
    # path("auth/", include("dj_rest_auth.urls")),
    # path("supervisor/interns/", UserAccountViewSet.as_view({"get": "get_interns"})),
]
