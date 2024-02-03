import os
import time
import zipfile

import imagesize
from api.models import File
from api.utils import get_compress_type_str
from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from PIL import Image, ImageStat


@shared_task(
    autoretry_for=(ObjectDoesNotExist,),
    retry_kwargs={"max_retries": 10, "countdown": 0.5},
)
def handle_file(file_id: int) -> bool:
    file = File.objects.get(pk=file_id)
    filepath = str(file.file.path)
    filename, file_extension = os.path.splitext(filepath)
    filename = filename.split("/")[-1]

    file.data = {
        "filename": filename,
        "extension": file_extension,
        "size": f"{round(os.path.getsize(filepath) / (1024 ** 2), 2)} MB",
    }

    if file_extension in [".png", ".jpg"]:
        img = Image.open(filepath)
        average_color = ImageStat.Stat(img).median
        file.data["photo"] = {
            "size": imagesize.get(filepath),
            "average_color_rgb": average_color[:3],
            "average_color_hex": "#" + "".join(f"{i:02x}" for i in average_color[:3]),
        }
    elif file_extension in [".zip"]:
        with zipfile.ZipFile(filepath, "r") as zf:
            num_files = len(zf.namelist())
            total_uncompressed_size = sum(zinfo.file_size for zinfo in zf.filelist)
            file.data["archive"] = {
                "files_amount": num_files,
                "total_uncompressed_size": total_uncompressed_size,
                "compression_type": get_compress_type_str(zf.compression),
                "compression_level": zf.compresslevel,
            }

    file.processed = True
    file.save()
    return True
