from rest_framework import serializers

from src.catalog.models import Book, Tag

from .tag import TagSerializer


class BookSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        source="tags",
        queryset=Tag.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "isbn",
            "author",
            "tags",
            "tag_ids",
        )
