from django.db import models
from anam_backend_main.constants import MessageType
# Create your models here.


class AttachedFile(models.Model):
    file = models.FileField('AttachedFiles', upload_to='attachedFiles')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    MessageTypeSelectChoice = (
        (MessageType.Normal.value, 'Normal'),
        (MessageType.BroadCast.value, 'Broadcast'),
    )
    attachedFiles = models.ManyToManyField('AttachedFile', related_name='messages', blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    child = models.ForeignKey('ChildApp.Child', on_delete=models.CASCADE, null=True, blank=True)
    sender = models.ForeignKey('UserApp.User', on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey('UserApp.User', on_delete=models.CASCADE, related_name='+')
    content = models.TextField()
    msgType = models.CharField(max_length=255, choices=MessageTypeSelectChoice,
                               default=MessageType.Normal)
    headerMessage = models.ForeignKey('Message', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
