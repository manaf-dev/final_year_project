from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from accounts.serializers.departments import DepartmentSerializer
from accounts.models.departments import Department


class DepartmentListCreateAPIView(ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
