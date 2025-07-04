from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone


class Cohort(models.Model):
    year = models.CharField(max_length=20, unique=True)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("upcoming", "Upcoming"),
            ("ongoing", "Ongoing"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="ongoing",
    )

    def __str__(self):
        return f"{self.year} internship cohort"

    class Meta:
        ordering = ["year", "start_date"]
