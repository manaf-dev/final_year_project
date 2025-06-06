from django.db import models
from django.contrib.auth.models import AbstractUser

from .departments import Department
# from .mentors import Mentor
# from .intern_schools import InternSchool
from internships.models import Cohort


class CustomUser(AbstractUser):
    TITLES = [
        ("mr", "Mr."),
        ("mrs", "Mrs."),
        ("miss", "Miss"),
        ("dr", "Dr."),
        ("prof", "Prof."),
    ]

    title = models.CharField(max_length=20, choices=TITLES, null=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    department = models.ForeignKey(
        Department, related_name="users", on_delete=models.SET_NULL, null=True
    )
    account_type = models.CharField(
        max_length=50,
        choices=[("intern", "Intern"), ("supervisor", "Supervisor")],
        null=True,
    )
    level = models.CharField(max_length=25, null=True, blank=True)
    supervisor = models.ForeignKey(
        "self", related_name="interns", on_delete=models.SET_NULL, null=True, blank=True
    )
    # intern_school = models.ForeignKey(
    #     InternSchool,
    #     verbose_name="Internship School",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    # )
    # mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True, blank=True)
    cohort = models.ForeignKey(
        Cohort, related_name="cohort_interns", on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return self.username
