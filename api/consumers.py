import json
from json.decoder import JSONDecodeError
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import DenyConnection

from django.contrib.auth.models import AnonymousUser

from .models import Message


GROUP_NAME = 'chat'


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        if self.scope['user'] == AnonymousUser():
            raise DenyConnection('Need authorization')

        async_to_sync(self.channel_layer.group_add)(
            GROUP_NAME,
            self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            GROUP_NAME,
            self.channel_name
        )

    def receive(self, text_data=None, bytes_data=None):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json['message']
        except JSONDecodeError:
            message = text_data

        async_to_sync(self.channel_layer.group_send)(
            GROUP_NAME,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def chat_message(self, event):
        message = event['message']
        user = self.scope['user']

        message_object = Message(text=message, author=user)
        message_object.save()
        message_id = message_object.id

        self.send(text_data=json.dumps({
            'message_id': message_id
        }))
