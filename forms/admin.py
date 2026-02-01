from django.contrib import admin

from .models import Form

@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    """Admin configuration for browsing and searching saved forms."""
    list_display = ("id", "user", "title", "pdf_bucket_url", "created_at", "updated_at")
    search_fields = ("id", "title", "pdf_bucket_url", "user__email")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
