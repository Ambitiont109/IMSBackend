import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import JsonWebsocketConsumer
from anam_backend_main.constants import Parent, Teacher, Admin
from .utils import get_user_sibling_group_name, get_user_channel_group_name


class NotificationConsumer(JsonWebsocketConsumer):
    groups = ["broadcast"]

    def connect(self):
        self.user = self.scope["user"]
        self.mygroups = []
        if self.user:
            if self.user.is_anonymous:
                self.close()
            else:
                print(self.user.id, ":", self.channel_name)
                if self.user.role == Parent:
                    sibling_group_name = get_user_sibling_group_name(self.user)
                    if sibling_group_name not in self.mygroups:
                        self.mygroups.append(sibling_group_name)
                    async_to_sync(self.channel_layer.group_add)(
                        sibling_group_name,
                        self.channel_name
                    )
                channel_group_name = get_user_channel_group_name(self.user)
                if channel_group_name not in self.mygroups:
                    self.mygroups.append(channel_group_name)
                async_to_sync(self.channel_layer.group_add)(
                    channel_group_name,
                    self.channel_name
                )
                if self.user.role not in self.mygroups:
                    self.mygroups.append(self.user.role)
                async_to_sync(self.channel_layer.group_add)(
                    self.user.role,
                    self.channel_name
                )
                self.accept()
                self.send_json(
                    {'message': {'data': {'verb': 'connect'}, 'group_name': channel_group_name}})
                print('groups:', self.mygroups)
        else:
            self.close()

    def disconnect(self, code):
        for group in self.mygroups:
            async_to_sync(self.channel_layer.group_discard)(
                group, self.channel_name
            )

    def receive_json(self, data):
        message = data['message']

        self.send_json({
            'message': message

        })

    def change_sibling_group(self, event):
        prev_group_id = event['prev_group_id']
        if prev_group_id:
            async_to_sync(self.channel_layer.group_discard)(
                str(prev_group_id)+"_group",
                self.channel_name
            )
        async_to_sync(self.channel_layer.group_discard)(
            get_user_sibling_group_name(self.user),
            self.channel_name
        )

    def send_message(self, event):
        print(self.mygroups)
        print(event)
        print(self.channel_name)
        message = event['message']
        self.send_json({'message': message})

    def broadcast_message(self, event):
        message = event['message']
        self.send_json({'message': message})
