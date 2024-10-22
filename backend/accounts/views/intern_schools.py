from ._base_imports import *

from accounts.serializers.intern_schools import InternSchoolSerializer
from accounts.models.intern_schools import InternSchool


class InternSchoolListCreateAPIView(ListCreateAPIView):
    queryset = InternSchool.objects.all()
    serializer_class = InternSchoolSerializer


class InternSchoolRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = InternSchool.objects.all()
    serializer_class = InternSchoolSerializer
