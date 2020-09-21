from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='message_as_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='message_as_receiver')
    reply_to = models.OneToOneField('Message', on_delete=models.CASCADE,
                                    related_name='replied_message')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
