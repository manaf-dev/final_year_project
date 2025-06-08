from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework import status


from .models import Cohort
from .serializers import CohortSerializer


class CohortViewSet(viewsets.ModelViewSet):
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=["get"])
    def cohorts(self, request):
        cohorts = Cohort.objects.all().distinct().order_by("-year")
        serializer = self.get_serializer(cohorts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        year = kwargs.get("year")
        cohort = Cohort.objects.filter(year=year).first()
        if not cohort:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(cohort)
        return Response(serializer.data, status=status.HTTP_200_OK)
