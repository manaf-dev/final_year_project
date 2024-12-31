from . import portfolios, submissions, comments, notifications


URL_COMPONENTS = (
    portfolios.PORTFOLIO_URLS
    + submissions.SUBMISSION_URLS
    + comments.COMMENT_URLS
    + notifications.NOTIFICATION_URLS
)


app_name = "submissions"

urlpatterns = URL_COMPONENTS
