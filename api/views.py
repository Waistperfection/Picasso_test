from django.db import transaction
from rest_framework import exceptions, generics

from api.tasks import process_file

from .models import File
from .serializers import FileSerializer, FileOutSerializer


class FileListView(generics.ListAPIView):
    queryset = File.objects.all()
    serializer_class = FileOutSerializer


class FileCreateView(generics.CreateAPIView):
    serializer_class = FileSerializer

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                instance = serializer.save()
                instance.save()
                kwargs = {"file_id": instance.id}
                transaction.on_commit(lambda: process_file.delay(**kwargs))
        except Exception as e:
            raise exceptions.APIException(str(e),)
