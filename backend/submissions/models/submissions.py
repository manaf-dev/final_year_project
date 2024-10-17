from django.db import models

from accounts.models.users import CustomUser


class Submission(models.Model):
    MONTHS = [
        ("1", "First Month"),
        ("2", "Second Month"),
        ("3", "Third Month"),
        ("4", "Fourth Month"),
    ]
    month = models.CharField(max_length=50, choices=MONTHS)
    intern = models.ForeignKey(
        CustomUser, related_name="week_submissions", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.intern.username} - {self.week} submission"


class Comment(models.Model):
    submission = models.ForeignKey(
        Submission, related_name="comments", on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment to {self.submission.intern.username}'s submission"
