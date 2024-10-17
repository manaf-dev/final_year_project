from django.db import models


class InternSchool(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    town = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    region = models.CharField(max_length=50)

    def __str__(self):
        return self.name
