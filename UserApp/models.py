from django.db import models
from django.contrib.auth.models import AbstractUser
from anam_backend_main.constants import Parent, Teacher, Admin, \
                                        Bamboo, Iroko, Baobab, Acajou
import json
# Create your models here.


class User(AbstractUser):
    USER_ROLE = [
        (Parent, 'Parent'),
        (Teacher, 'Teacher'),
        (Admin, 'Admin')
    ]
    role = models.CharField(max_length=10, choices=USER_ROLE, default=Parent)
    picture = models.ImageField(upload_to="upload/photo", null=True, blank=True)
    classnames = models.CharField(null=True, blank=True, max_length=255)
    phoneNumber = models.CharField(null=True, blank=True, max_length=255)
    address = models.CharField(null=True, blank=True, max_length=255)

    def get_classNames(self):
        try:
            data = json.loads(self.classnames)
            if(type(data) == type([])):
                return data
            return []
        except Exception:
            return []
