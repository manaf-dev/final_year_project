from django.urls import path

from .views import submissionview


urlpatterns = [
    path("", submissionview),
]
