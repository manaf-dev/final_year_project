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
    path("submissions/upload/cv/", SubmissionViewSet.as_view({"post": "upload_cv"})),
    path(
        "submissions/submit/video/",
        SubmissionViewSet.as_view({"post": "submit_video"}),
    ),
    path(
        "submissions/cohort/<str:year>/<int:month>/",
        SubmissionViewSet.as_view({"get": "get_cohort_month_submissions"}),
    ),
    path(
        "submissions/cohort/<str:year>/count/",
        SubmissionViewSet.as_view({"get": "get_submissions_count"}),
    ),
]
