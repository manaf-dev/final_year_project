from ._base_imports import *
from django.utils import timezone
from django.db.models import Count, Q
from accounts.models.users import UserAccount
from accounts.selectors.users import (
    get_interns_by_supervisor,
    user_representation,
    get_supervisor_interns_by_cohort,
)
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
    get_submission_video_by_id,
    get_submission_video_by_submission,
)
from submissions.selectors.portfolios import (
    get_portfolio_file_by_submission_and_type,
)
from internships.selectors import get_cohort_by_id, get_cohort_by_year
from submissions.models.portfolios import PortfolioImage, PortfolioFile


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_intern_submissions(self, request):
        intern = request.user
        if intern.account_type != "intern":
            return Response(
                {"detail": "You cannot perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        submissions = filter_submissions_by_intern(intern.id)
        context = {"graded_submissions": submissions.filter(graded=True).count()}

        images = PortfolioImage.objects.filter(submission__in=submissions).count()
        files = PortfolioFile.objects.filter(submission__in=submissions).count()
        video = SubmissionVideo.objects.filter(submission__in=submissions).count()
        context["portfolio_count"] = images + files + video

        return Response(context, status=status.HTTP_200_OK)

    def get_existing_submissions(self, request):
        intern = request.user
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
        return submission

    def upload_img(self, request):
        """
        Uploads image files to the portfolio
        """
        submission = self.get_existing_submissions(request)

        portfolio_imgs = request.FILES.getlist("file")
        portfolio_images_data = [
            {"image": img, "submission": submission.id} for img in portfolio_imgs
        ]
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

    def upload_document(self, request):
        """
        Unified method to upload portfolio documents (CV, Philosophy, Reflective)
        Supports both new uploads and updates of existing documents
        """
        # Get document type from request data
        document_type = request.data.get("type")
        if not document_type:
            return Response(
                {"detail": "Document type is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate document type
        valid_types = ["cv", "teaching_philosophy", "reflective"]
        if document_type not in valid_types:
            return Response(
                {
                    "detail": f"Invalid document type. Must be one of: {', '.join(valid_types)}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get or create submission
        submission = self.get_existing_submissions(request)

        # Get uploaded file
        uploaded_files = request.FILES.getlist("file")
        if not uploaded_files:
            return Response(
                {"detail": "No file provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        document_file = uploaded_files[0]

        # Check if document of this type already exists for this submission
        existing_document = get_portfolio_file_by_submission_and_type(
            submission.id, document_type
        )

        # Prepare document data
        document_data = {
            "submission": submission.id,
            "file_type": document_type,
            "file": document_file,
        }

        # Get user-friendly type names for response messages
        type_names = {
            "cv": "CV",
            "teaching_philosophy": "Teaching Philosophy",
            "reflective": "Reflective Teaching Statement",
        }
        type_name = type_names.get(document_type, document_type.title())

        try:
            if existing_document:
                # Update existing document
                file_serializer = PortfolioFileSerializer(
                    existing_document, data=document_data, partial=True
                )
                file_serializer.is_valid(raise_exception=True)
                file_serializer.save()

                return Response(
                    {"detail": f"{type_name} updated successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                # Create new document
                file_serializer = PortfolioFileSerializer(data=document_data)
                file_serializer.is_valid(raise_exception=True)
                file_serializer.save()

                return Response(
                    {"detail": f"{type_name} uploaded successfully"},
                    status=status.HTTP_201_CREATED,
                )

        except Exception as e:
            return Response(
                {"detail": f"Error saving {type_name.lower()}", "error": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def check_document_exists(self, request):
        """
        Check if a specific document type exists for a submission
        """
        intern = request.user
        if intern.account_type != "intern":
            return Response(
                {"detail": "You cannot perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        month = request.query_params.get("month")
        document_type = request.query_params.get("type")

        if not month or not document_type:
            return Response(
                {"detail": "Month and document type are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Get submission for this month
        submission = get_submission_by_intern(intern.id, month=month)
        if not submission:
            return Response(
                {"exists": False, "document": None},
                status=status.HTTP_200_OK,
            )

        # Check if document exists
        existing_document = get_portfolio_file_by_submission_and_type(
            submission.id, document_type
        )

        if existing_document:
            from submissions.serializers.portfolios import PortfolioFileSerializer

            serializer = PortfolioFileSerializer(existing_document)
            return Response(
                {"exists": True, "document": serializer.data},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"exists": False, "document": None},
                status=status.HTTP_200_OK,
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
            serializer = SubmissionVideoSerializer(
                submission_video,
                data=video_data,
                partial=True,
                context={"request": request},
            )
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

    def get_cohort_scores(self, request, cohort_id):
        supervisor = self.is_supervisor(request)
        cohort = get_cohort_by_id(cohort_id)
        if not cohort:
            return Response(
                {"detail": "Cohort not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        cohort_interns = get_supervisor_interns_by_cohort(supervisor.id, cohort.id)
        if not cohort_interns:
            return Response(
                {"detail": "No interns scores for this cohort"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Group scores by intern, then by month
        # [{'intern': {}, 'scores': {'1': 85, '2': 90, '3': 88}}]
        scores = []
        for intern in cohort_interns:
            grades = {"id": intern.id, "intern": user_representation(intern)}
            submissions = self.queryset.filter(intern=intern)
            for month in range(1, 5):
                for submission in submissions:
                    if submission.month == str(month):
                        grades[f"month_{month}"] = (
                            submission.grade if submission.graded else None
                        )
                        break
                    grades[f"month_{month}"] = -1

            scores.append(grades)

        return Response(scores, status=status.HTTP_200_OK)

    def delete_video(self, request, video_id):
        submission_video = get_submission_video_by_id(video_id)
        if not submission_video:
            return Response(
                {"detail": "Video not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        submission_video.delete()
        return Response(
            {"detail": "Video deleted successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )
