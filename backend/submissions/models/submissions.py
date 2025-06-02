from django.db import models

from accounts.models.users import CustomUser


class Submission(models.Model):
    MONTHS = [
        ("1", "First Month"),
        ("2", "Second Month"),
        ("3", "Third Month"),
        ("4", "Fourth Month"),
    ]
    month = models.CharField(max_length=10, choices=MONTHS)
    intern = models.ForeignKey(
        CustomUser, related_name="submissions", on_delete=models.CASCADE
    )
    grade = models.PositiveIntegerField(default=0, null=True, blank=True)
    graded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.intern.username} - month {self.month} submission"


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser, null=True, blank=True, on_delete=models.CASCADE
    )
    submission = models.ForeignKey(
        Submission, related_name="comments", on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment to {self.submission.intern.username}'s submission"


# class Grade(models.Model):
#     mark = models.PositiveIntegerField(default=0)
#     submission = models.ForeignKey(
#         Submission, related_name="grades", on_delete=models.CASCADE
#     )
#     graded_at = models.DateTimeField(auto_now=True)


class SubmissionVideo(models.Model):
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
