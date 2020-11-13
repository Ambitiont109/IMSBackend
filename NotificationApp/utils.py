from channels.layers import get_channel_layer
from django.db.models import Q
from asgiref.sync import async_to_sync
from anam_backend_main.constants import Parent, Teacher, Admin
from .models import Notification, NotificationStatusRecord, NotificationVerb
from MessageApp.views import check_user_unreadness
from .serializers import NotificationReadSerializer, NotificationStatusRecordSerializer


def get_user_sibling_group_name(user):
    if user.child:
        return 'sibling_group_' + str(user.child.sibling_group.id)
    return 'anonymous'


def get_user_channel_group_name(user):
    return str(user.id) + '_group'


def change_parent_sibling_group(prev_group_id, user):
    channel_group_name = get_user_channel_group_name(user)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(channel_group_name, {
        "type": "change_sibling_group", "prev_group_id": prev_group_id})


def send_broadcast():
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "broadcast", {"type": "broadcast_message", "message": "Test World"})


def send_to_user_channel(user, message):
    if user:
        channel_group_name = get_user_channel_group_name(user)
        if user.role == Parent:
            channel_group_name = get_user_sibling_group_name(user)
        # if user.role == Admin:
        #     channel_group_name = Admin
        print(channel_group_name)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            channel_group_name, {"type": "send_message", "message": message})


def message_create_notification(message):
    # notification = Notification(
    #     sender=message.sender, verb=NotificationVerb.MessageCreate, subject='New Message', content=message.content)
    # notification.save()
    # record = NotificationStatusRecord(
    #     notification=notification, receiver=message.receiver)
    # record.save()
    channel_message = {
        "data": {
            "verb": NotificationVerb.MessageCreate,
            "sender": message.sender.id,
        },
        "receiver": message.receiver.id
    }
    send_to_user_channel(message.receiver, channel_message)


def create_notification_record(receiver, notification):
    serializer = NotificationReadSerializer(notification)
    channel_message = {
        "data": serializer.data,
        "receiver": receiver.id
    }
    send_to_user_channel(receiver, channel_message)


def message_read_notification(user):
    channel_message = {
            "data": {
                "verb": NotificationVerb.UnreadMessage,
                "sender": user.id,
            },
            "receiver": user.id
        }
    if check_user_unreadness(user):
        send_to_user_channel(user, channel_message)
    else:
        channel_message['data']['verb'] = NotificationVerb.NoMessage
        send_to_user_channel(user, channel_message)
