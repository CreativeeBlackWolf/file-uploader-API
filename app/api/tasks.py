from celery import shared_task

from api.models import File
import os


@shared_task
def handle_file(file_id: int) -> bool:
    file = File.objects.get(id=file_id)
    filename, file_extension = os.path.splitext(str(file.file.path))

    file.data = {
        "filename": filename,
        "extension": file_extension,
    }

    file.processed = True
    file.save()
    return True
