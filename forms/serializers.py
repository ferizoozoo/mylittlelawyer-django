from rest_framework import serializers

from .models import Form


class FormSerializer(serializers.ModelSerializer):
    """Serialize Form records for API responses and input validation."""
    class Meta:
        model = Form
        fields = ("id", "user", "title", "pdf_bucket_url", "created_at", "updated_at")
        read_only_fields = ("id", "created_at", "updated_at")
