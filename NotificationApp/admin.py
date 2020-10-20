from django.contrib import admin
from .models import Notification, NotificationStatusRecord
# Register your models here.
admin.site.register(Notification)
admin.site.register(NotificationStatusRecord)
