from django.urls import path

from submissions.views.submissions import *


SUBMISSION_URLS = [
    path(
        "submissions/intern/",
        SubmissionViewSet.as_view({"get": "get_intern_submissions"}),
    ),
    path("submissions/upload/img/", SubmissionViewSet.as_view({"post": "upload_img"})),
    path(
        "submissions/upload/philosophy/",
        SubmissionViewSet.as_view({"post": "upload_philosophy"}),
    ),
    path(
        "submissions/upload/cv/",
        SubmissionViewSet.as_view({"post": "upload_cv"}),
    ),
    path(
        "interns/submissions/<int:month>/",
        SubmissionViewSet.as_view({"get": "get_interns_month_submissions"}),
    ),
    path(
        "submissions/to-supervisor/",
        SubmissionViewSet.as_view({"get": "get_submissions_toSupervisor"}),
    ),
]
