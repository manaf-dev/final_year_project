from submissions.models.submissions import Submission
from submissions.models.portfolios import PortfolioImage

from submissions.serializers.submissions import SubmissionSerializer
from submissions.serializers.portfolios import PortfolioImageSerializer


def get_submission_by_intern(intern_id: int, month):
    try:
        submission = Submission.objects.get(intern=intern_id, month=month)
        return submission
    except:
        return None


def get_submission_by_id(submission_id: int):
    return Submission.objects.get(id=submission_id)
