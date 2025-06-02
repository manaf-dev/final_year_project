from ._base_imports import *
from django.utils import timezone
from django.db.models import Count, Q
from accounts.models.users import CustomUser
from accounts.selectors.users import get_interns_by_supervisor
from submissions.models.submissions import Submission, SubmissionVideo
from submissions.serializers.submissions import (
    SubmissionSerializer,
    SubmissionVideoSerializer,
)
from submissions.serializers.portfolios import (
    PortfolioFileSerializer,
    PortfolioImageSerializer,
)

from submissions.selectors.submissions import (
    get_submission_by_intern,
    get_submission_by_id,
    filter_submissions_by_intern,
    get_submission_video_by_submission,
)
from accounts.selectors.users import get_user_by_id
from internships.selectors import get_cohort_by_year


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_intern_submissions(self, request):
        intern = request.user
        submissions = filter_submissions_by_intern(intern.id).order_by("month")
        try:
            submissions_data = self.get_serializer(submissions, many=True).data
            return Response(submissions_data, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error fetching intern submissions:", e)
            return Response(
                {"detail": "Error fetching intern submissions"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
            submission_data = serializer.save()
            submission = get_submission_by_id(submission_data.data.get("id"))
            print("New submission created:", submission)

        return submission

    def upload_img(self, request):
        """
        Uploads image files to the portfolio
        """
        submission = self.get_existing_submissions(request)

        portfolio_imgs = request.FILES.getlist("file")
        print("Portfolio images:", portfolio_imgs)
        portfolio_images_data = [
            {"image": img, "submission": submission.id} for img in portfolio_imgs
        ]
        print("Portfolio images data:", portfolio_images_data)
        portfolio_serializer = PortfolioImageSerializer(
            data=portfolio_images_data, many=True
        )
        portfolio_serializer.is_valid(raise_exception=True)

        try:
            portfolio_serializer.save()
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
            return True, file_serializer.data
        # except file_serializer.ValidationError as e:
        #     print("Error saving file:", e)
        #     return False, file_serializer.errors
        except Exception as e:
            return False, str(e)

    def upload_philosophy(self, request):
        submission = self.get_existing_submissions(request)

        philosophy_file = request.data.getlist("file")[0]
        print("Philosophy:", philosophy_file)

        if not philosophy_file:
            return Response(
                {"detail": "Philosophy file not sent"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        philosophy = {
            "submission": submission.id,
            "file_type": "teaching_philosophy",
            "file": philosophy_file,
        }

        file_save, errors = self.save_file(philosophy)

        if file_save:
            return Response(
                {"detail": "Teaching Philosophy upload successful"},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"detail": "Error saving file", "errors": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def upload_cv(self, request):
        submission = self.get_existing_submissions(request)

        cv_file = request.data.getlist("file")[0]
        print("CV:", cv_file)

        if not cv_file:
            return Response(
                {"detail": "CV file not sent"}, status=status.HTTP_400_BAD_REQUEST
            )

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

    def is_supervisor(self, request):
        supervisor = request.user

        if supervisor.account_type != "supervisor":
            return Response(
                {"detail": "You cannot perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        return supervisor

    def get_cohort_month_submissions(self, request, year, month):
        supervisor = self.is_supervisor(request)
        cohort = get_cohort_by_year(year=year)

        interns = get_interns_by_supervisor(supervisor.id)
        cohort_interns = interns.filter(cohort=cohort)
        print("cohort_interns", cohort_interns)
        interns_submissions = self.queryset.filter(
            month=month, intern__in=cohort_interns
        ).order_by("created_at")
        serializer = self.get_serializer(interns_submissions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_submissions_count(self, request, year):
        supervisor = self.is_supervisor(request)
        cohort = get_cohort_by_year(year=year)

        interns = get_interns_by_supervisor(supervisor.id)
        cohort_interns = interns.filter(cohort=cohort)

        counts = self.queryset.filter(intern__in=cohort_interns).aggregate(
            submissions_count=Count("id"),
            graded_submissions_count=Count("id", filter=Q(graded=True)),
        )
        counts = {
            "submissions_count": counts.get("submissions_count", 0),
            "graded_submissions_count": counts.get("graded_submissions_count", 0),
            "interns_count": cohort_interns.count(),
        }
        return Response(counts, status=status.HTTP_200_OK)

    def submit_video(self, request):
        submission = self.get_existing_submissions(request)

        video_url = request.data.get("video_url")
        if not video_url:
            return Response(
                {"detail": "Video URL not provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        video_data = {"video_url": video_url, "submission": submission.id}

        submission_video = get_submission_video_by_submission(submission.id)
        if submission_video:
            serializer = SubmissionVideoSerializer(data=video_data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(
                    {"detail": "Video submitted successfully"},
                    status=status.HTTP_200_OK,
                )

            return Response(
                {"detail": "Error submitting video"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = SubmissionVideoSerializer(data=video_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {"detail": "Video submitted successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"detail": "Error submitting video"},
            status=status.HTTP_400_BAD_REQUEST,
        )
