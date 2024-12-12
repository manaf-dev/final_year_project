from django.urls import path

from submissions.views.portfolios import *

from submissions.views.comments import CommentViewSet

COMMENT_URLS = [
    path("comment/create/", CommentViewSet.as_view({"post": "create_comment"}))
]
