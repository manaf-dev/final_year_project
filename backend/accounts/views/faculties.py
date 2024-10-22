from ._base_imports import *

from accounts.serializers.faculties import FacultySerializer
from accounts.models.faculties import Faculty


class FacultyListCreateAPIView(ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class FacultyRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
