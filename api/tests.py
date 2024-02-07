from pathlib import Path
import shutil
from django.conf import settings

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings

from rest_framework import status
from rest_framework.test import APITestCase

from .models import File
from .serializers import FileSerializer, FileOutSerializer
from unittest.mock import patch


TEST_DIR = settings.BASE_DIR / "test_dir"


class FileAPITests(APITestCase):

    def test_list_files(self):
        # Создаем несколько файлов в базе данных
        File.objects.create(file="file1.txt")
        File.objects.create(file="file2.jpg")
        File.objects.create(file="file3.pdf")
        # Получаем список файлов через API
        url = reverse("files")
        response = self.client.get(url)
        # Проверяем статус ответа и количество файлов
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        # Проверяем, что данные файлов соответствуют сериализатору
        files = File.objects.all()
        serializer = FileOutSerializer(files, many=True)
        self.assertEqual(response.data, serializer.data)

    # Тест для проверки загрузки файла
    # Для предотвращения перезаписи существующих файлов - переопределяем MEDIA_ROOT
    @override_settings(MEDIA_ROOT=TEST_DIR)
    def test_upload_file(self):

        # Создаем объект файла
        tmp_file = SimpleUploadedFile(
            "file.jpg", b"file_content", content_type="image/jpg"
        )

        # Отправляем POST-запрос с файлом через API
        url = reverse("upload")
        response = self.client.post(url, {"file": tmp_file}, format="multipart")

        # Проверяем статус ответа и данные файла
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["file"], "http://testserver/uploads/file.jpg")
        self.assertEqual(response.data["processed"], False)

        # Проверяем, что файл создан в базе данных
        self.assertEqual(File.objects.count(), 1)
        self.assertEqual(File.objects.get().file.name, "uploads/file.jpg")

        # проверяем наличие загруженного файла в файловой системе
        full_file_path: Path = Path(settings.MEDIA_ROOT) / File.objects.get().file.name
        self.assertEqual(full_file_path.exists(), True)

        self.assertEqual(File.objects.get().processed, False)

    # Тест для проверки обработки файла
    def test_process_file(self):
        # Создаем файл в базе данных
        file = File.objects.create(file="file1.txt")
        # Запускаем функцию симулирующую обработку файла
        from .tasks import process_file
        import inspect

        process_file(file.id)
        # Проверяем, что поле processed изменилось на True
        file.refresh_from_db()
        self.assertEqual(file.processed, True)
        # TODO Добавить тест маппинга функции обработки файла

    @override_settings(MEDIA_ROOT=settings.BASE_DIR / "test_dir")
    def test_deleting_file_with_model_record(self):
        tmp_file = SimpleUploadedFile(
            "new_file.jpg", b"file_content", content_type="image/jpg"
        )

        file = File.objects.create(file=tmp_file)
        path_to_file = Path(settings.MEDIA_ROOT) / file.file.name
        self.assertEqual(path_to_file.exists(), True)
        file.delete()
        self.assertEqual(path_to_file.exists(), False)

    @classmethod
    def tearDownClass(cls):
        print("\nDeleting temporary files...\n")
        try:
            shutil.rmtree(TEST_DIR)
        except FileNotFoundError:
            pass
