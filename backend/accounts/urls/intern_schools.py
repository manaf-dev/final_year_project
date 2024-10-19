from django.urls import path

from accounts.views import intern_schools

INTERN_SCHOOLS_URLS = [path("intern-schools/", intern_schools.intern_schools, name="")]
