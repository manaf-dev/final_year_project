from re import sub
from ._base_imports import *
from itertools import chain
from django.db.models import Q

from accounts.selectors.users import get_user_by_username
from submissions.models.portfolios import PortfolioFile, PortfolioImage
from submissions.serializers.portfolios import (
    PortfolioFileSerializer,
    PortfolioImageSerializer,
)
from submissions.serializers.comments import CommentSerializer
from submissions.serializers.submissions import (
    SubmissionSerializer,
    SubmissionVideoSerializer,
)

from submissions.selectors.submissions import (
    get_submission_by_intern,
    filter_submissions_by_intern,
)
from submissions.selectors.portfolios import (
    get_portfolio_images_by_submission,
    get_portfolio_files_by_submission,
    get_portfolio_images_by_id,
    get_portfolio_file_by_id,
)
from submissions.selectors.comments import get_comments
from submissions.models.submissions import SubmissionVideo


class PortfolioViewset(viewsets.ModelViewSet):
    queryset = PortfolioImage.objects.all()
    serializer_class = PortfolioImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_month_portfolio(self, request, username, month):
        """
        Get portfolio images and files for a specific month
        """

        intern = get_user_by_username(username)
        if not intern:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        submission = get_submission_by_intern(intern, month)
        if not submission:
            return Response(
                {"detail": "No submission found"}, status=status.HTTP_200_OK
            )

        portfolio_imgs = get_portfolio_images_by_submission(submission.id)

        portfolio_files = (
            get_portfolio_files_by_submission(submission.id) if month == 4 else None
        )

        context = SubmissionSerializer(submission).data

        if portfolio_imgs:
            portfolio_imgs_data = self.get_serializer(
                portfolio_imgs, many=True, context={"request": request}
            ).data
            context["images"] = portfolio_imgs_data

        if portfolio_files:
            portfolio_files_data = PortfolioFileSerializer(
                portfolio_files, many=True, context={"request": request}
            ).data
            context["files"] = portfolio_files_data

        comments = get_comments(submission.id)
        if comments:
            comments_data = CommentSerializer(comments, many=True).data
            context["comments"] = comments_data

        return Response(context, status=status.HTTP_200_OK)

    def delete_portfolio_img(self, request, portfolio_id):
        """
        Delete a portfolio image
        """

        portfolio_img = get_portfolio_images_by_id(portfolio_id)

        if portfolio_img:
            portfolio_img.delete()
            return Response(
                {"detail": "Portfolio deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"detail": "Portfolio image found"}, status=status.HTTP_404_NOT_FOUND
            )

    def delete_portfolio_file(self, request, portfolio_id):
        print("id", portfolio_id)
        portfolio_file = get_portfolio_file_by_id(portfolio_id)

        if portfolio_file:
            portfolio_file.delete()
            return Response(
                {"detail": "Document deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
        else:
            return Response(
                {"detail": "Portfolio file found"}, status=status.HTTP_404_NOT_FOUND
            )


class PortfolioList(viewsets.ModelViewSet):
    serializer_class = PortfolioImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def recent_portfolio(self, request):
        intern = request.user
        submissions = filter_submissions_by_intern(intern.id)

        images = PortfolioImage.objects.filter(submission__in=submissions).order_by(
            "-uploaded_at"
        )[:2]

        files = PortfolioFile.objects.filter(submission__in=submissions).order_by(
            "-uploaded_at"
        )[:2]

        combined_items = sorted(
            chain(images, files), key=lambda x: x.uploaded_at, reverse=True
        )[:2]

        if not combined_items:
            return Response(
                {"detail": "No portfolio items submitted."},
                status=status.HTTP_200_OK,
            )

        # Serialize items based on their type
        serialized_items = []
        for item in combined_items:
            if isinstance(item, PortfolioImage):
                serializer = PortfolioImageSerializer(
                    item, context={"request": request}
                )
            else:
                serializer = PortfolioFileSerializer(item, context={"request": request})

            serialized_items.append(serializer.data)

        return Response(serialized_items, status=status.HTTP_200_OK)

    def all_portfolio(self, request):
        intern = request.user
        submissions = filter_submissions_by_intern(intern.id)
        images = PortfolioImage.objects.filter(submission__in=submissions).order_by(
            "-uploaded_at"
        )
        files = PortfolioFile.objects.filter(submission__in=submissions).order_by(
            "-uploaded_at"
        )

        if not images and not files:
            return Response(
                {"detail": "No portfolio images or files Submitted."},
                status=status.HTTP_200_OK,
            )
        images_data = self.get_serializer(
            images, many=True, context={"request": request}
        ).data
        files_data = PortfolioFileSerializer(
            files, many=True, context={"request": request}
        ).data

        context = {"images": images_data, "files": files_data}

        if SubmissionVideo.objects.filter(submission__in=submissions).exists():
            video = SubmissionVideo.objects.filter(submission__in=submissions).first()
            context["video"] = SubmissionVideoSerializer(video).data
        else:
            context["video"] = None

        return Response(context, status=status.HTTP_200_OK)

    def total_portfolio_count(self, request):
        intern = request.user
        submissions = filter_submissions_by_intern(intern.id)
        images = PortfolioImage.objects.filter(submission__in=submissions).count()
        files = PortfolioFile.objects.filter(submission__in=submissions).count()
        context = {"portfolio_count": images + files}
        return Response(context, status=status.HTTP_200_OK)
