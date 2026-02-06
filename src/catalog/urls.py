from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"books", views.BookViewSet, basename="book")
router.register(r"tags", views.TagViewSet, basename="tag")
router.register(r"book-changes", views.BookChangeViewSet, basename="book-change")

urlpatterns = [
    path("", include(router.urls)),
]
