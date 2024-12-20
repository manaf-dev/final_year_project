from ._base_imports import *

from submissions.models.submissions import Comment, Submission
from submissions.serializers.comments import CommentSerializer
from submissions.serializers.submissions import SubmissionSerializer
from submissions.selectors.submissions import get_submission_by_id

from submissions.utils.notifications import create_notification


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create_comment(self, request):
        print("Data:", request.data)
        supervisor = request.user
        if supervisor.account_type != "supervisor":
            return Response(
                {"detail": "You cannot perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        submission = get_submission_by_id(request.data.get("submission_id"))
        if not submission:
            return Response(
                {"detail": "Submission not found"}, status=status.HTTP_404_NOT_FOUND
            )

        grade = request.data.get("grade")
        if grade != "":
            submission_serializer = SubmissionSerializer(
                submission, data={"grade": grade, "graded": True}, partial=True
            )
            submission_serializer.is_valid(raise_exception=True)
            submission_serializer.save()

        comment_data = {
            "supervisor": supervisor.id,
            "content": request.data.get("content"),
            "submission": submission.id,
        }
        comment_serializer = self.get_serializer(data=comment_data)
        comment_serializer.is_valid(raise_exception=True)
        comment_serializer.save()

        if grade:
            create_notification(
                supervisor.id,
                submission.intern,
                title="Comment and grade on your Submission",
                content="Your supervisor has commentted and graded your portfolio submission. You should Check it out",
            )
        else:
            create_notification(
                receiver=submission.intern,
                title="Comment on your Submission",
                content="Your supervisor has commentted on your portfolio submission. You should Check it out",
            )

        return Response(
            {"detail": "Review Submitted Successfully"},
            status=status.HTTP_201_CREATED,
        )
