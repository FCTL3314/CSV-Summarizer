from django.db import models
from django.core.validators import FileExtensionValidator


class CSVFile(models.Model):
    file = models.FileField(
        upload_to='csv_files/',
        validators=[
            FileExtensionValidator(allowed_extensions=['csv'])
        ]
    )

    def __str__(self):
        return f'{self.file.name} | {self.file.path}'
