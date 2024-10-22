from django.urls import path

from .views import *


urlpatterns = [
    path("submissions/", SubmissionViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "submission/<int:pk>/",
        SubmissionViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    # COMMENTS
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
    # PORTFOLIO IMAGES
    path(
        "portfolio-imgs/",
        PortfolioImageViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "portfolio-img/<int:pk>/",
        PortfolioImageViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
    # PORTFOLIO FILES
    path(
        "portfolio-files/",
        PortfolioFileViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "portfolio-file/<int:pk>/",
        PortfolioFileViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
]
