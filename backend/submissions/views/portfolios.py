from ._base_imports import *


from submissions.models.portfolios import PortfolioFile, PortfolioImage
from submissions.serializers.portfolios import (
    PortfolioFileSerializer,
    PortfolioImageSerializer,
)

from submissions.selectors.submissions import get_submission_by_intern
from submissions.selectors.portfolios import get_portfolio_by_submission


class PortfolioFileViewSet(viewsets.ModelViewSet):
    queryset = PortfolioFile.objects.all()
    serializer_class = PortfolioFileSerializer
    # permission_classes = []


class PortfolioImageViewSet(viewsets.ModelViewSet):
    queryset = PortfolioImage.objects.all()
    serializer_class = PortfolioImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_month_imgs(self, request, month):
        intern = request.user
        submission = get_submission_by_intern(intern.id, month)
        if not submission:
            return Response(
                {"detail": "No submission found"}, status=status.HTTP_404_NOT_FOUND
            )

        portfolio_imgs = get_portfolio_by_submission(submission.id)
        if portfolio_imgs:
            portfolio_imgs_data = self.get_serializer(portfolio_imgs, many=True).data
            return Response(portfolio_imgs_data, status=status.HTTP_200_OK)

        return Response(
            {"detail": "Portfolio not found"}, status=status.HTTP_404_NOT_FOUND
        )
