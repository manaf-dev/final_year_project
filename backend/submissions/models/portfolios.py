from django.db import models

from .submissions import Submission


class PortfolioImage(models.Model):
    submission = models.ForeignKey(
        Submission, related_name="portfolio_imgs", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="portfolio_imgs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)


class PortfolioFile(models.Model):
    FILE_TYPES = [
        ("teaching_philosophy", "Teaching Philosophy"),
        ("reflective_writing", "Reflective writing"),
        ("cv", "Curriculum Vitae (CV)"),
    ]

    submission = models.ForeignKey(
        Submission, related_name="files", on_delete=models.CASCADE
    )
    file_type = models.CharField(max_length=50, choices=FILE_TYPES, default="file")
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
