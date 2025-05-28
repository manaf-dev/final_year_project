from submissions.models.submissions import Submission, SubmissionVideo
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
    try:
        return Submission.objects.get(id=submission_id)
    except:
        return None


def filter_submissions_by_intern(intern_id):
    return Submission.objects.filter(intern=intern_id)


def get_submission_video_by_id(video_id):
    try:
        return SubmissionVideo.objects.get(id=video_id)
    except:
        return None


def get_submission_video_by_submission(submission_id):
    try:
        return SubmissionVideo.objects.get(submission=submission_id)
    except:
        return None
