import uuid
from django.db import models

from accounts.models.users import UserAccount


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    receiver = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
