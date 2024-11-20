from django.db import models
from datetime import datetime, timedelta


class InternshipPeriod(models.Model):
    year = models.CharField(max_length=20)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(default=datetime.now() + timedelta(days=120))

    def __str__(self):
        return f"{self.academic_year} internship"
