from django.db import models
from django.contrib.auth.models import AbstractUser

from .departments import Department
from .mentors import Mentor
from .intern_schools import InternSchool


class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    department = models.ForeignKey(
        Department, related_name="users", on_delete=models.SET_NULL, null=True
    )
    supervisor_account = models.BooleanField(default=False)
    intern_account = models.BooleanField(default=False)
    supervisor = models.ForeignKey(
        "self", related_name="interns", on_delete=models.SET_NULL, null=True, blank=True
    )
    intern_school = models.ForeignKey(
        InternSchool,
        verbose_name="Internship School",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username
