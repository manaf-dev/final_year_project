from django.urls import path

from submissions.views.submissions import *


SUBMISSION_URLS = [
    path("submissions/", SubmissionViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "submission/<int:pk>/",
        SubmissionViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    path(
        "submission/comments/",
        CommentViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "submission/comment/<int:pk>/",
        CommentViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
]
