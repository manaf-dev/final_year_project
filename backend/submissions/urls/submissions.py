from django.urls import path

from submissions.views.submissions import *


SUBMISSION_URLS = [
    path("submissions/", SubmissionViewSet.as_view({"get": "list"})),
    path("submissions/upload/", SubmissionViewSet.as_view({"post": "upload_img"})),
    path(
        "submission/<int:pk>/",
        SubmissionViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path(
        "submission/intern/<str:username>/",
        SubmissionViewSet.as_view({"get": "intern_month_submissions"}),
    ),
    path(
        "submission/<int:submission_id>/comments/",
        CommentViewSet.as_view({"get": "list"}),
    ),
    path(
        "submission/comment/post/",
        CommentViewSet.as_view({"post": "create"}),
    ),
    path(
        "submission/comment/<int:pk>/",
        CommentViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
]
