from django.urls import path

from submissions.views.submissions import *


SUBMISSION_URLS = [
    path(
        "intern/",
        SubmissionViewSet.as_view({"get": "get_intern_submissions"}),
    ),
    path("upload/images/", SubmissionViewSet.as_view({"post": "upload_img"})),
    path(
        "upload/document/",
        SubmissionViewSet.as_view({"post": "upload_document"}),
    ),
    path(
        "document/check/",
        SubmissionViewSet.as_view({"get": "check_document_exists"}),
    ),
    path(
        "submit/video/",
        SubmissionViewSet.as_view({"post": "submit_video"}),
    ),
    path(
        "video/<str:video_id>/delete/",
        SubmissionViewSet.as_view({"delete": "delete_video"}),
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
    # New grading system URLs
    path(
        "grades/cohort/<str:cohort_id>/",
        SubmissionViewSet.as_view({"get": "get_new_cohort_scores"}),
    ),
    path(
        "grades/intern/<str:intern_id>/",
        SubmissionViewSet.as_view({"get": "get_intern_grades"}),
    ),
    path(
        "grades/portfolio/update/",
        SubmissionViewSet.as_view({"post": "update_portfolio_score"}),
    ),
    path(
        "grades/teaching-philosophy/update/",
        SubmissionViewSet.as_view({"post": "update_teaching_philosophy_score"}),
    ),
    path(
        "grades/reflective-practice/update/",
        SubmissionViewSet.as_view({"post": "update_reflective_practice_score"}),
    ),
]
