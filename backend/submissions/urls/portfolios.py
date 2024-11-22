from django.urls import path

from submissions.views.portfolios import *


PORTFOLIO_URLS = [
    path(
        "portfolio/<int:month>/",
        PortfolioViewset.as_view({"get": "get_month_portfolio"}),
    ),
    path("portfolio/recents/", PortfolioList.as_view({"get": "recent_portfolio"})),
    path("portfolio/all/", PortfolioList.as_view({"get": "all_portfolio"})),
]
