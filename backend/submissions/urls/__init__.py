from . import portfolios, submissions


URL_COMPONENTS = portfolios.PORTFOLIO_URLS + submissions.SUBMISSION_URLS


app_name = "submissions"

urlpatterns = URL_COMPONENTS
