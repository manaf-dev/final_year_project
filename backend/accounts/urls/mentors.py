from django.urls import path

from accounts.views.mentors import MentorViewSet


MENTORS_URLS = [
    path("mentors/all/", MentorViewSet.as_view({"get": "list"})),
    path("mentor/<int:id>/", MentorViewSet.as_view({"get": "retrieve"})),
    path("mentor/create/", MentorViewSet.as_view({"post": "create_mentor"})),
    path("mentors/update/", MentorViewSet.as_view({"put": "update"})),
]
