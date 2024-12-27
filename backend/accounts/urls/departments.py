from django.urls import path

from accounts.views.departments import (
    DepartmentListCreateAPIView,
    DepartmentRetrieveUpdateDestroyAPIView,
)

DEPARTMENTS_URLS = [
    path("departments/", DepartmentListCreateAPIView.as_view()),
    path("department/<int:pk>/", DepartmentRetrieveUpdateDestroyAPIView.as_view()),
]
