from django.db import models
from anam_backend_main.constants import Classroom, All
# Create your models here.


class SchoolDocument(models.Model):
    ForSelect = [
        (Classroom, 'Classroom'),
        (All, 'All'),
    ]
    name = models.CharField(max_length=255)
    url = models.FileField(upload_to='schooldocument')
    documentfor = models.CharField(max_length=255, choices=ForSelect,
                                   default=All)
    is_new = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


