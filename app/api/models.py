from django.db import models
import uuid


class File(models.Model):
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    data = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.file}:{self.uploaded_at.date()}"
