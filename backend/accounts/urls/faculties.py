from django.urls import path

from accounts.views.faculties import (
    FacultyListCreateAPIView,
    FacultyRetrieveUpdateDestroyAPIView,
)

FACULTIES_URLS = [
    path("faculties/", FacultyListCreateAPIView.as_view()),
    path("faculty/<int:pk>/", FacultyRetrieveUpdateDestroyAPIView.as_view()),
]
