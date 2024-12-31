from django.urls import path
from .views import CohortViewSet


urlpatterns = [
    path("cohorts/", CohortViewSet.as_view({"get": "years"})),
    path("cohorts/create/", CohortViewSet.as_view({"post": "create"})),
    path("cohorts/update/", CohortViewSet.as_view({"put": "update"})),
]
