from django.urls import path

from accounts.views.mentors import (
    MentorListCreateAPIView,
    MentorRetrieveUpdateDestroyAPIView,
)

MENTORS_URLS = [
    path(
        "mentors/",
        MentorListCreateAPIView.as_view(),
        name="mentor-list-create",
    ),
    path(
        "mentor/<int:pk>/",
        MentorRetrieveUpdateDestroyAPIView.as_view(),
        name="mentor-retrieve",
    ),
]
