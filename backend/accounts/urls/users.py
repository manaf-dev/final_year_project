from django.urls import path, include

from accounts.views.users import CustomUserViewSet, CustomRegisterView, CustomLoginView

USERS_URLS = [
    path("auth/login/", CustomLoginView.as_view()),
    # path("auth/", include("dj_rest_auth.urls")),
    path("auth/registration/", CustomRegisterView.as_view()),
    path("users/", CustomUserViewSet.as_view({"get": "list"}), name="list-users"),
    path(
        "user/<int:pk>/",
        CustomUserViewSet.as_view({"get": "retrieve"}),
        name="retrieve-user",
    ),
    path(
        "user/<int:pk>/update/",
        CustomUserViewSet.as_view({"put": "update"}),
        name="update-user",
    ),
    path(
        "user/<int:pk>/delete/",
        CustomUserViewSet.as_view({"delete": "destroy"}),
        name="delete-user",
    ),
    path(
        "supervisor/<int:supervisor_id>/interns/",
        CustomUserViewSet.as_view({"get": "get_supervisor_interns"}),
        name="supervisor-interns",
    ),
]
