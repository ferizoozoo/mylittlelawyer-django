import uuid
from django.db import models
from accounts.models import User

class Form(models.Model):
    """Metadata for a saved PDF form stored in GCP for a specific user."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forms")
    pdf_bucket_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "forms"

    def __str__(self) -> str:
        """Readable identifier for admin screens and logs."""
        return f"Form {self.id}"
