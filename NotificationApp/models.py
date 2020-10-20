from django.db import models
# Create your models here.


class NotificationVerb(models.TextChoices):
    MessageCreate = 'message_create'
    UnreadMessage = 'there_is_unreadmessage'
    NoMessage = 'no_message'
    UNREAD = "unread"


class Notification(models.Model):
    """docstring for Profile"""
    verb = models.CharField(max_length=255, null=True)
    subject = models.CharField(max_length=255)
    content = models.CharField(max_length=200, default="default messsage")
    sender = models.ForeignKey('UserApp.User', on_delete=models.CASCADE)
    receivers = models.ManyToManyField(
        'UserApp.User', through='NotificationStatusRecord', related_name='received_notifications')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationStatusRecord(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        'UserApp.User', on_delete=models.CASCADE, related_name="received_notification_status")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
