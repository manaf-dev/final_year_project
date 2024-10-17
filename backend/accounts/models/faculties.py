from django.db import models


class Faculty(models.Model):
    name = models.CharField(max_length=255)
    faculty_code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "faculty"
        verbose_name_plural = "faculties"
