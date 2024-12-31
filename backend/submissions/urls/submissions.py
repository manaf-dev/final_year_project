from django.urls import path

from submissions.views.submissions import *


SUBMISSION_URLS = [
    path("intern/", SubmissionViewSet.as_view({"get": "get_intern_submissions"})),
    path("upload/img/", SubmissionViewSet.as_view({"post": "upload_img"})),
    path(
        "upload/philosophy/", SubmissionViewSet.as_view({"post": "upload_philosophy"})
    ),
    path("upload/cv/", SubmissionViewSet.as_view({"post": "upload_cv"})),
    path(
        "cohort/<str:cohort>/<int:month>/",
        SubmissionViewSet.as_view({"get": "get_cohort_submissions"}),
    ),
    path(
        "to-supervisor/",
        SubmissionViewSet.as_view({"get": "get_submissions_toSupervisor"}),
    ),
]
