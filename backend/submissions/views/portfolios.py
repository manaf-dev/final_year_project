from ._base_imports import *


from submissions.models.portfolios import PortfolioFile, PortfolioImage
from submissions.serializers.portfolios import (
    PortfolioFileSerializer,
    PortfolioImageSerializer,
)


class PortfolioFileViewSet(viewsets.ModelViewSet):
    queryset = PortfolioFile.objects.all()
    serializer_class = PortfolioFileSerializer
    # permission_classes = []


class PortfolioImageViewSet(viewsets.ModelViewSet):
    queryset = PortfolioImage.objects.all()
    serializer_class = PortfolioImageSerializer
    # permission_classes = []
