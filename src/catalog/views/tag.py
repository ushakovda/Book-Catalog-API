from rest_framework import viewsets

from src.catalog.models import Tag
from src.catalog.serializers import TagSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
