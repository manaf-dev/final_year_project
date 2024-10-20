from django.urls import path

from accounts.views.intern_schools import (
    InternSchoolListCreateAPIView,
    InternSchoolRetrieveUpdateDestroyAPIView,
)

INTERN_SCHOOLS_URLS = [
    path(
        "intern-schools/",
        InternSchoolListCreateAPIView.as_view(),
        name="intern-school-list-create",
    ),
    path(
        "intern-school/<int:pk>/",
        InternSchoolRetrieveUpdateDestroyAPIView.as_view(),
        name="intern-school-retrieve",
    ),
]
