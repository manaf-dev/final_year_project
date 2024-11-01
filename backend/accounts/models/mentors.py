from django.db import models

from .intern_schools import InternSchool


class Mentor(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return self.name
