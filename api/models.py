from pathlib import Path

from django.conf import settings
from django.db import models


class File(models.Model):
    file = models.FileField("file", upload_to="uploads/", unique=True)
    uploaded_at = models.DateTimeField("upload time", auto_now_add=True)
    processed = models.BooleanField(default=False)

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"
        ordering = ("uploaded_at",)

    # TODO del file after delete record from db
    def delete(self, *args, **kwargs):
        full_path: Path = settings.MEDIA_ROOT / self.file.name
        super().delete(*args, **kwargs)
        try:
            full_path.unlink()
        except FileNotFoundError:
            pass
            # TODO
