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
        grade = request.data.get("grade")
        comment = request.data.get("content")

        if supervisor.account_type != "supervisor":
            return Response(
                {"detail": "You cannot perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        if not grade and not comment:
            return Response(
                {"detail": "You must provide either a grade or a comment"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        submission = get_submission_by_id(request.data.get("submission_id"))
        if not submission:
            return Response(
                {"detail": "Submission not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if grade != "":
            submission_serializer = SubmissionSerializer(
                submission, data={"grade": grade, "graded": True}, partial=True
            )
            submission_serializer.is_valid(raise_exception=True)
            submission_serializer.save()

        if comment != "":
            comment_data = {
                "supervisor": supervisor.id,
                "content": comment,
                "submission": submission.id,
            }
            comment_serializer = self.get_serializer(data=comment_data)
            comment_serializer.is_valid(raise_exception=True)
            comment_serializer.save()

        if grade and comment:
            create_notification(
                receiver=submission.intern,
                title="Comment and grade on your Submission",
                content="Your supervisor has commentted and graded your portfolio submission. You should Check it out",
            )
        elif grade and not comment:
            create_notification(
                receiver=submission.intern,
                title="Grade on your Submission",
                content="Your supervisor has graded your portfolio submission. You should Check it out",
            )
        elif not grade and comment:
            create_notification(
                receiver=submission.intern,
                title="Comment on your Submission",
                content="Your supervisor has commentted on your portfolio submission. You should Check it out",
            )
        else:
            create_notification(
                receiver=submission.intern,
                title="Review on your Submission",
                content="Your supervisor has reviewed on your portfolio submission. You should Check it out",
            )

        return Response(
            {"detail": "Review Submitted Successfully"},
            status=status.HTTP_201_CREATED,
        )
