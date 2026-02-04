from django.db import models

from .tag import Tag


class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=32, unique=True)
    author = models.CharField(max_length=255)
    tags = models.ManyToManyField(Tag, blank=True, related_name="books")
