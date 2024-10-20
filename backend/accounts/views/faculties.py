from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from accounts.serializers.faculties import FacultySerializer
from accounts.models.faculties import Faculty


class FacultyListCreateAPIView(ListCreateAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer


class FacultyRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
