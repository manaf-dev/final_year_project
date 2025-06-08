from django.urls import path

from submissions.views.submissions import *


SUBMISSION_URLS = [
    path(
        "intern/",
        SubmissionViewSet.as_view({"get": "get_intern_submissions"}),
    ),
    path("upload/img/", SubmissionViewSet.as_view({"post": "upload_img"})),
    path(
        "upload/philosophy/",
        SubmissionViewSet.as_view({"post": "upload_philosophy"}),
    ),
    path("upload/cv/", SubmissionViewSet.as_view({"post": "upload_cv"})),
    path(
        "submit/video/",
        SubmissionViewSet.as_view({"post": "submit_video"}),
    ),
    path(
        "cohort/<str:year>/<int:month>/",
        SubmissionViewSet.as_view({"get": "get_cohort_month_submissions"}),
    ),
    path(
        "cohort/<str:year>/count/",
        SubmissionViewSet.as_view({"get": "get_submissions_count"}),
    ),
    path(
        "scores/cohort/<str:cohort_id>/",
        SubmissionViewSet.as_view({"get": "get_cohort_scores"}),
    ),
]
