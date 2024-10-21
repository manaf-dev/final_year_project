from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from accounts.models.mentors import Mentor
from accounts.serializers.mentors import MentorSerializer


class MentorListCreateAPIView(ListCreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer


class MentorRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
