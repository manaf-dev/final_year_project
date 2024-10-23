from submissions.models.submissions import Submission
from submissions.models.portfolios import PortfolioImage

from submissions.serializers.submissions import SubmissionSerializer
from submissions.serializers.portfolios import PortfolioImageSerializer


def get_month_submission_by_intern(intern_id: int, month):
    month_submissions = Submission.objects.filter(intern=intern_id, month=month)
    submissions = SubmissionSerializer(month_submissions, many=True).data

    for submission in submissions:
        submission_imgs = PortfolioImage.objects.filter(submission=submission["id"])
        submission["images"] = PortfolioImageSerializer(submission_imgs, many=True).data

    return submissions


def get_submission_by_id(submission_id: int):
    return Submission.objects.get(id=submission_id)