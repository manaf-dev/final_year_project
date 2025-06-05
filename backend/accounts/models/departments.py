import uuid
from django.db import models

from .faculties import Faculty


class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    department_code = models.CharField(max_length=50, unique=True)
    faculty = models.ForeignKey(
        Faculty, related_name="departments", on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
