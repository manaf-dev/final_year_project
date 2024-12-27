from django.db import models


class InternSchool(models.Model):
    school = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=100, null=True)
    district = models.CharField(max_length=100, null=True)
    region = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.school
