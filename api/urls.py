# Добавляем URL-пути для API в urls.py
from django.urls import path
from .views import FileCreateView, FileListView


urlpatterns = [
    path("upload/", FileCreateView.as_view(), name="upload"),
    path("files/", FileListView.as_view(), name="files"),
]
