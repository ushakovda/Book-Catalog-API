from rest_framework.viewsets import ReadOnlyModelViewSet

from src.catalog.models import BookChangeLog
from src.catalog.serializers import BookChangeLogSerializer


class BookChangeViewSet(ReadOnlyModelViewSet):
    serializer_class = BookChangeLogSerializer

    def get_queryset(self):
        qs = BookChangeLog.objects.all()
        book_id = self.request.query_params.get("book_id")
        if book_id:
            qs = qs.filter(book_id=book_id)
        return qs
