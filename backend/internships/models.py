from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone


class Cohort(models.Model):
    year = models.CharField(max_length=20, unique=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=datetime.now() + timedelta(days=120))

    def __str__(self):
        return f"{self.year} internship cohort"

    class Meta:
        ordering = ["year", "start_date"]
