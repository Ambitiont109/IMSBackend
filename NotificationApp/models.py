from django.db import models
# Create your models here.


class NotificationVerb(models.TextChoices):
    MessageCreate = 'message_create'
    UnreadMessage = 'there_is_unreadmessage'
    NoMessage = 'no_message'
    UNREAD = "unread"
    Normal = 'Normal'


class Notification(models.Model):
    """docstring for Profile"""
    verb = models.CharField(max_length=255, null=True)
    subject = models.CharField(max_length=255)
    content = models.CharField(max_length=200, default="default messsage")
    sender = models.ForeignKey('UserApp.User', on_delete=models.CASCADE, related_name='sent_notifications')
    receivers = models.ManyToManyField(
        'UserApp.User', through='NotificationStatusRecord', related_name='received_notifications')
    is_child_broadcast = models.BooleanField(default=False)
    is_teacher_broadcast = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationStatusRecord(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='notification_status_list')
    receiver = models.ForeignKey(
        'UserApp.User', on_delete=models.CASCADE, related_name="received_notification_status")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
