from django.db import models

from .intern_schools import InternSchool


class Mentor(models.Model):
    name = models.CharField(max_length=255)
    school = models.ForeignKey(
        InternSchool, related_name="mentors", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
