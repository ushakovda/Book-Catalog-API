from rest_framework import serializers

from src.catalog.models import BookChangeLog


class BookChangeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookChangeLog
        fields = (
            "id",
            "book_id",
            "field_name",
            "old_value",
            "new_value",
            "created_at",
        )
        read_only_fields = fields
