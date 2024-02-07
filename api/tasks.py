from time import sleep
from celery import shared_task

from api.models import File
from utils import handler


@shared_task
def process_file(file_id):
    file = File.objects.get(id=file_id)
    try:
        handler(file)
        sleep(5)  # TODO Удалить после добавления необходимой логики
    except Exception:  # TODO Тут надо отлавлиавть кастомные исключения обработки файлов
        return
    else:
        file.processed = True
        file.save()
