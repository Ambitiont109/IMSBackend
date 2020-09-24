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


# class Appointment(models.Model):
#     teacher = models.ForeignKey(User, on_delete=models.CASCADE)
#     parent = models.ForeignKey(User, on_delete=models.CASCADE)

#     time_start = models.DateTimeField()
#     time_end = models.DateTimeField()
#     confirmed = models.BooleanField(default=False)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     # show filed in admin panel

#     def __str__(self):
#         return self.time_start
