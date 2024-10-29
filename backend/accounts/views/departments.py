from ._base_imports import *

from accounts.serializers.departments import DepartmentSerializer
from accounts.models.departments import Department


class DepartmentListCreateAPIView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DepartmentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
