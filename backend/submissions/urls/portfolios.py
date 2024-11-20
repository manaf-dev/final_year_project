from django.urls import path

from submissions.views.portfolios import *


PORTFOLIO_URLS = [
    path(
        "portfolio/<int:month>/",
        PortfolioViewset.as_view({"get": "get_month_portfolio"}),
    ),
    path(
        "portfolio-imgs/",
        PortfolioViewset.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "portfolio-img/<int:pk>/",
        PortfolioViewset.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
    ),
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
