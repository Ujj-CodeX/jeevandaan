
import uuid
from django.db import models

class RefreshToken(models.Model):
    token_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    user_type = models.CharField(max_length=10)  # 'donor' or 'partner'
    user_id = models.IntegerField()
    is_revoked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    replaced_by = models.UUIDField(null=True, blank=True)  # naya token jo isse replace kiya

    class Meta:
        indexes = [models.Index(fields=['token_id'])]
        