import uuid
from django.db import models

from .submissions import Submission


class PortfolioImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.ForeignKey(
        Submission, related_name="portfolio_imgs", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="portfolio_imgs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} for Submission {self.submission.id} by {self.submission.intern.username}"


class PortfolioFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    FILE_TYPES = [
        ("teaching_philosophy", "Teaching Philosophy"),
        ("reflective", "Reflective Teaching Statement"),
        ("cv", "Curriculum Vitae (CV)"),
    ]

    submission = models.ForeignKey(
        Submission, related_name="files", on_delete=models.CASCADE
    )
    file_type = models.CharField(max_length=50, choices=FILE_TYPES, default="file")
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"File {self.id} ({self.file_type}) for Submission {self.submission.id} by {self.submission.intern.username}"
