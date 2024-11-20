from ._base_imports import *


from submissions.models.portfolios import PortfolioFile, PortfolioImage
from submissions.serializers.portfolios import (
    PortfolioFileSerializer,
    PortfolioImageSerializer,
)

from submissions.selectors.submissions import get_submission_by_intern
from submissions.selectors.portfolios import (
    get_portfolio_images_by_submission,
    get_portfolio_files_by_submission,
)


class PortfolioFileViewSet(viewsets.ModelViewSet):
    queryset = PortfolioFile.objects.all()
    serializer_class = PortfolioFileSerializer
    permission_classes = [permissions.IsAuthenticated]


class PortfolioViewset(viewsets.ModelViewSet):
    queryset = PortfolioImage.objects.all()
    serializer_class = PortfolioImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_month_portfolio(self, request, month):
        intern = request.user
        print("int:", intern.id, "mon:", month)
        submission = get_submission_by_intern(intern.id, month)
        if not submission:
            return Response(
                {"detail": "No submission found"}, status=status.HTTP_404_NOT_FOUND
            )

        portfolio_imgs = get_portfolio_images_by_submission(submission.id)

        portfolio_files = (
            get_portfolio_files_by_submission(submission.id) if month == 4 else None
        )

        if portfolio_imgs or portfolio_files:
            portfolio_imgs_data = self.get_serializer(portfolio_imgs, many=True).data

            portfolio_files_data = PortfolioFileSerializer(
                portfolio_files, many=True
            ).data
            context = {
                "images": portfolio_imgs_data,
                "files": portfolio_files_data,
                "graded": submission.graded,
            }
            return Response(context, status=status.HTTP_200_OK)

        return Response(
            {"detail": "Portfolio not found"}, status=status.HTTP_404_NOT_FOUND
        )
