from django.urls import path, include

from accounts.views.users import (
    CustomUserListCreateAPIView,
    CustomUserRetrieveUpdateDestroyAPIView,
)

USERS_URLS = [
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", include("dj_rest_auth.registration.urls")),
    path("users/", CustomUserListCreateAPIView.as_view(), name="user-list-create"),
    path(
        "user/<int:pk>/",
        CustomUserRetrieveUpdateDestroyAPIView.as_view(),
        name="user-retrieve",
    ),
]
