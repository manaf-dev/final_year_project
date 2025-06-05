import uuid
from django.db import models
from accounts.models.users import UserAccount


class Submission(models.Model):
    MONTHS = [
        ("1", "First Month"),
        ("2", "Second Month"),
        ("3", "Third Month"),
        ("4", "Fourth Month"),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    month = models.CharField(max_length=10, choices=MONTHS)
    intern = models.ForeignKey(
        UserAccount, related_name="submissions", on_delete=models.CASCADE
    )
    grade = models.PositiveIntegerField(default=0, null=True, blank=True)
    graded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.intern.username} - month {self.month} submission"


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    supervisor = models.ForeignKey(
        UserAccount, null=True, blank=True, on_delete=models.CASCADE
    )
    submission = models.ForeignKey(
        Submission, related_name="comments", on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment to {self.submission.intern.username}'s submission"


class SubmissionVideo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    submission = models.OneToOneField(
        Submission,
        on_delete=models.CASCADE,
        related_name="video",
        null=False,
        blank=False,
    )
    video_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Video for {self.submission.intern.username}'s submission"
