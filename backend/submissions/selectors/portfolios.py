from submissions.models import PortfolioImage


def get_portfolio_by_submission(submission_id):
    try:
        images = PortfolioImage.objects.filter(submission=submission_id)
        return images
    except:
        return None
