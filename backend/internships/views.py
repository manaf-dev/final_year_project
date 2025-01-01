from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action

from .models import Cohort
from .serializers import CohortSerializer


class CohortViewSet(viewsets.ModelViewSet):
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"])
    def years(self, request):
        cohorts = Cohort.objects.all().distinct()
        serializer = self.get_serializer(cohorts, many=True)
        return Response(serializer.data)
