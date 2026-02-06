from rest_framework import viewsets
from rest_framework.response import Response

from src.catalog.models import Book
from src.catalog.serializers import BookSerializer
from src.catalog.services.book_change_logger import BookUpdateContext, BookUpdateService


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.prefetch_related("tags").all()
    serializer_class = BookSerializer

    TRACKED_FIELDS = ("title", "isbn", "author")

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        context = BookUpdateContext(
            instance=instance,
            serializer=serializer,
            tracked_fields=self.TRACKED_FIELDS,
            tag_ids_were_provided=("tag_ids" in request.data),
        )

        service = BookUpdateService(
            context=context,
            perform_update=self.perform_update,
        )
        service.execute()

        return Response(serializer.data)
