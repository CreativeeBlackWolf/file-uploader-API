from celery import shared_task

from api.models import File
import os
import time
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection


@shared_task(
    autoretry_for=(ObjectDoesNotExist,),
    retry_kwargs={"max_retries": 10, "countdown": 0.5},
)
def handle_file(file_id: int) -> bool:
    time.sleep(0.1)  # slow down to make sure that DB was updated
    file = File.objects.get(pk=file_id)
    filepath = str(file.file.path)
    filename, file_extension = os.path.splitext(filepath)

    file.data = {
        "filename": filename,
        "extension": file_extension,
        "size": f"{round(os.path.getsize(filepath) / (1024 ** 2), 2)}",
    }

    file.processed = True
    file.save()
    return True
