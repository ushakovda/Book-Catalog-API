from django.db import models

from .book import Book


class BookChangeLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="change_logs")
    field_name = models.CharField(max_length=64)
    old_value = models.JSONField(null=True, blank=True)
    new_value = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
