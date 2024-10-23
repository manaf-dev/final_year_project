from ._base_imports import *

from accounts.models.users import CustomUser
from submissions.models.submissions import Submission, Comment
from submissions.serializers.submissions import SubmissionSerializer, CommentSerializer

from submissions.selectors.submissions import (
    get_month_submission_by_intern,
    get_submission_by_id,
)
from accounts.selectors.users import get_user_by_username


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer

    def intern_month_submissions(self, request, username):
        user = get_user_by_username(username)
        if not user:
            context = {
                "detail": "User account not found",
                "errors": [f"User account '{username}'  does not exist"],
            }
            raise NotFound(context)

        queryset = get_month_submission_by_intern(
            user.id, self.request.query_params.get("month")
        )
        return Response(queryset)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def list(self, request, submission_id, *args, **kwargs):
        submission = get_submission_by_id(submission_id)
        submission_post = SubmissionSerializer(submission).data

        comments = submission.comments.all()
        post_comments = CommentSerializer(comments, many=True).data

        submission_post["comments"] = [comment["content"] for comment in post_comments]
        return Response(submission_post)
