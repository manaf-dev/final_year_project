from ._base_imports import *

from accounts.models.users import CustomUser
from submissions.models.submissions import Submission, Comment
from submissions.serializers.submissions import SubmissionSerializer, CommentSerializer
from submissions.serializers.portfolios import (
    PortfolioFileSerializer,
    PortfolioImageSerializer,
)

from submissions.selectors.submissions import (
    get_submission_by_intern,
    get_submission_by_id,
    filter_submissions_by_intern,
)
from accounts.selectors.users import get_user_by_id


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_intern_submissions(self, request):
        intern = request.user
        submissions = filter_submissions_by_intern(intern.id).order_by("month")
        if submissions:
            submissions_data = self.get_serializer(submissions, many=True).data
            return Response(submissions_data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"detail": "No submission found"}, status=status.HTTP_404_NOT_FOUND
            )

    def get_existing_submissions(self, request):
        intern = request.user
        print(request.data)
        submission = get_submission_by_intern(
            intern.id, month=request.data.get("month")
        )

        # Create a new submission if none exists
        if not submission:
            serializer = self.get_serializer(
                data={"month": request.data.get("month"), "intern": intern.id}
            )
            serializer.is_valid(raise_exception=True)
            submission = serializer.save()
            print("New submission created:", submission)

        return submission

    def upload_img(self, request):

        submission = self.get_existing_submissions(request)

        # Access multiple files for 'portfolio_imgs'
        portfolio_imgs = request.FILES.getlist("files")
        portfolio_images_data = [
            {"image": img, "submission": submission.id} for img in portfolio_imgs
        ]

        print("Portfolio images data to be serialized:", portfolio_images_data)

        portfolio_serializer = PortfolioImageSerializer(
            data=portfolio_images_data, many=True
        )
        portfolio_serializer.is_valid(raise_exception=True)

        try:
            portfolio_serializer.save()
            print("Portfolio images saved successfully.")
        except Exception as e:
            print("Error saving portfolio images:", e)

        return Response(
            {"detail": "Portfolio images upload successful"},
            status=status.HTTP_201_CREATED,
        )

    def save_file(self, file):

        try:
            file_serializer = PortfolioFileSerializer(data=file)
            file_serializer.is_valid(raise_exception=True)
            file_serializer.save()
            return True
        except Exception as e:
            return False

    def upload_philosophy(self, request):
        submission = self.get_existing_submissions(request)

        philosophy_file = request.data.get("files")
        print("Philosophy:", philosophy_file)

        if not philosophy_file:
            return Response({"detail": "Philosophy file not sent"})

        philosophy = {
            "submission": submission.id,
            "file_type": "teaching_philosophy",
            "file": philosophy_file,
        }

        file_save = self.save_file(philosophy)

        if file_save:
            return Response(
                {"detail": "Teaching Philosophy upload successful"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"detail": "Error saving file"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def upload_cv(self, request):
        submission = self.get_existing_submissions(request)

        cv_file = request.data.get("files")
        print("CV:", cv_file)

        if not cv_file:
            return Response({"detail": "CV file not sent"})

        cv = {
            "submission": submission.id,
            "file_type": "cv",
            "file": cv_file,
        }

        file_save = self.save_file(cv)

        return Response(
            {"detail": "CV upload successful"},
            status=status.HTTP_201_CREATED,
        )


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
