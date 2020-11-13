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


class MiniClub(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField(max_length=255)
    price = models.FloatField()
    limit = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    children = models.ManyToManyField('ChildApp.Child', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BookStatus(models.TextChoices):
    PRESENT = 'present'
    RENTED = 'rented'


class ExchangeLibrary(models.Model):
    title = models.CharField(max_length=255)
    picture = models.ImageField(upload_to='exchangelibrary')
    child = models.ForeignKey('ChildApp.Child', blank=True, null=True, on_delete=models.SET_NULL)
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, choices=BookStatus.choices, default=BookStatus.PRESENT)
    donator = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Marketing(models.Model):
    question = models.CharField(max_length=255)
    content = models.TextField()
    poster = models.ForeignKey('UserApp.User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)