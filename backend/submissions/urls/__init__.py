from . import portfolios, submissions, comments


URL_COMPONENTS = (
    portfolios.PORTFOLIO_URLS + submissions.SUBMISSION_URLS + comments.COMMENT_URLS
)


app_name = "submissions"

urlpatterns = URL_COMPONENTS
