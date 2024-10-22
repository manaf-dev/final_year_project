from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from submissions.models.submissions import Submission, Comment
from submissions.models.portfolios import PortfolioFile, PortfolioImage
from submissions.serializers.submissions import SubmissionSerializer, CommentSerializer
from submissions.serializers.portfolios import (
    PortfolioFileSerializer,
    PortfolioImageSerializer,
)


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []


class PortfolioFileViewSet(viewsets.ModelViewSet):
    queryset = PortfolioFile.objects.all()
    serializer_class = PortfolioFileSerializer
    # permission_classes = []


class PortfolioImageViewSet(viewsets.ModelViewSet):
    queryset = PortfolioImage.objects.all()
    serializer_class = PortfolioImageSerializer
    # permission_classes = []
