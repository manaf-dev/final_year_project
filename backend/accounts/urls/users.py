from django.urls import path, include

from accounts.views.users import CustomUserViewSet, CustomRegisterView, CustomLoginView

USERS_URLS = [
    path("auth/login/", CustomLoginView.as_view()),
    path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", CustomRegisterView.as_view()),
    path("users/", CustomUserViewSet.as_view({"get": "list"})),
    path("user/<int:pk>/info/", CustomUserViewSet.as_view({"get": "retrieve"})),
    path("user/<int:pk>/update/", CustomUserViewSet.as_view({"put": "update"})),
    path(
        "user/<int:pk>/update-school/",
        CustomUserViewSet.as_view({"put": "update_school"}),
    ),
    path("user/<int:pk>/delete/", CustomUserViewSet.as_view({"delete": "destroy"})),
    path("supervisor/interns/", CustomUserViewSet.as_view({"get": "get_interns"})),
]
