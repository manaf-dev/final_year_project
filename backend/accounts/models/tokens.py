import uuid
from django.db import models
from django.utils import timezone
from .users import UserAccount


class Token(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        UserAccount, on_delete=models.CASCADE, related_name="tokens"
    )
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_revoked = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)

    def __str__(self):
        return f"Token {self.token} for user {self.user.username}"
