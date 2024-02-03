from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class File(models.Model):
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.file}:{self.uploaded_at.date()}"


@receiver(post_save, sender=File, dispatch_uid="handle_file")
def handle_file_after_save(sender, instance, **kwargs):
    if instance.processed == False:
        from api.tasks import handle_file

        handle_file.delay(instance.id)
