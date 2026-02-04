from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Optional, Sequence

from django.db import transaction
from rest_framework.serializers import BaseSerializer

from src.catalog.models import Book, BookChangeLog


@dataclass(frozen=True)
class BookUpdateContext:
    instance: Book
    serializer: BaseSerializer
    tracked_fields: Sequence[str]
    tag_ids_were_provided: bool


class BookUpdateService:
    def __init__(
        self,
        *,
        context: BookUpdateContext,
        perform_update: Callable[[BaseSerializer], None],
    ) -> None:
        self._context = context
        self._perform_update = perform_update
        self._instance = context.instance

    def execute(self) -> Book:
        """
        Выполняет обновление Book и логирование изменений.
        """
        old_fields = self._get_field_snapshot(
            self._instance, self._context.tracked_fields
        )
        old_tags = (
            self._get_tag_ids(self._instance)
            if self._context.tag_ids_were_provided
            else None
        )

        with transaction.atomic():
            self._perform_update(self._context.serializer)
            self._instance.refresh_from_db()

            logs = []
            logs.extend(self._build_field_logs(old_fields))
            logs.extend(self._build_tag_logs(old_tags))

            if logs:
                BookChangeLog.objects.bulk_create(logs)

        return self._instance

    @staticmethod
    def _get_field_snapshot(instance: Book, fields: Iterable[str]) -> dict[str, Any]:
        return {name: getattr(instance, name) for name in fields}

    @staticmethod
    def _get_tag_ids(instance: Book) -> list[int]:
        return list(instance.tags.values_list("id", flat=True))

    def _build_field_logs(self, old_fields: dict[str, Any]) -> list[BookChangeLog]:
        logs: list[BookChangeLog] = []

        for field in self._context.tracked_fields:
            new_value = getattr(self._instance, field)
            if old_fields[field] != new_value:
                logs.append(
                    BookChangeLog(
                        book=self._instance,
                        field_name=field,
                        old_value=old_fields[field],
                        new_value=new_value,
                    )
                )

        return logs

    def _build_tag_logs(self, old_tags: Optional[list[int]]) -> list[BookChangeLog]:
        if old_tags is None:
            return []

        new_tags = self._get_tag_ids(self._instance)
        if set(old_tags) == set(new_tags):
            return []

        return [
            BookChangeLog(
                book=self._instance,
                field_name="tags",
                old_value=old_tags,
                new_value=new_tags,
            )
        ]
