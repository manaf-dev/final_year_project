from submissions.models import PortfolioImage, PortfolioFile


def get_portfolio_images_by_submission(submission_id):
    try:
        images = PortfolioImage.objects.filter(submission=submission_id)
        return images
    except:
        return None


def get_portfolio_files_by_submission(submission_id):
    try:
        files = PortfolioFile.objects.filter(submission=submission_id)
        return files
    except:
        return None


def get_portfolio_images_by_id(portfolio_id):
    try:
        image = PortfolioImage.objects.get(id=portfolio_id)
        return image
    except:
        return None


def get_portfolio_file_by_id(portfolio_id):
    try:
        file = PortfolioFile.objects.get(id=portfolio_id)
        return file
    except:
        return None
