from ._base_imports import *

from submissions.models.submissions import Submission, Comment
from submissions.serializers.submissions import SubmissionSerializer, CommentSerializer



class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = []
