import os
import time

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
app = Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task
def debug_task():
    time.sleep(10)
    print("horray!")
    return True
