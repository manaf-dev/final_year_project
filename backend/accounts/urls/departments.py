from django.urls import path

from accounts.views import departments

DEPARTMENTS_URLS = [
    path("departments/", departments.departments, name=""),
]
