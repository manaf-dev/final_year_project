from django.urls import path

from submissions.views.portfolios import *


PORTFOLIO_URLS = [
    path(
        "portfolio/<str:username>/<int:month>/",
        PortfolioViewset.as_view({"get": "get_month_portfolio"}),
    ),
    path("portfolio/recents/", PortfolioList.as_view({"get": "recent_portfolio"})),
    path("portfolio/all/", PortfolioList.as_view({"get": "all_portfolio"})),
    path(
        "portfolio/count-all/", PortfolioList.as_view({"get": "total_portfolio_count"})
    ),
    path(
        "portfolio/img/delete/<int:portfolio_id>/",
        PortfolioViewset.as_view({"delete": "delete_portfolio_img"}),
    ),
    path(
        "portfolio/file/delete/<int:portfolio_id>/",
        PortfolioViewset.as_view({"delete": "delete_portfolio_file"}),
    ),
]
