from django.urls import path

from accounts.views.intern_schools import InternSchoolViewSet


INTERN_SCHOOLS_URLS = [
    path(
        "intern-schools/all/",
        InternSchoolViewSet.as_view({"get": "list"}),
    ),
    path(
        "intern-school/<int:id>/",
        InternSchoolViewSet.as_view({"get": "retrieve"}),
    ),
    path(
        "intern-school/new/",
        InternSchoolViewSet.as_view({"post": "new_intern_school"}),
    ),
    path(
        "intern-school/update/<int:id>/",
        InternSchoolViewSet.as_view({"put": "update"}),
    ),
]
