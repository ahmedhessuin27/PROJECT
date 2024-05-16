# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from .models import ChatRequest

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Authenticate user
        if self.scope['user'].is_anonymous:
            await self.close()
        else:
            self.user = self.scope['user']
            self.room_group_name = f'user_{self.user.id}'
            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'send_chat_request':
            receiver_id = data.get('receiver_id')
            await self.send_chat_request(receiver_id)

    async def send_chat_request(self, receiver_id):
        try:
            receiver = User.objects.get(id=receiver_id)
            chat_request = ChatRequest.objects.create(sender=self.user, receiver=receiver)
            # Send notification to the receiver
            await self.channel_layer.group_send(
                f'user_{receiver_id}',
                {
                    'type': 'notify_request',
                    'sender_id': self.user.id,
                    'sender_username': self.user.username,
                }
            )
        except User.DoesNotExist:
            # Handle case where receiver user does not exist
            pass

    async def notify_request(self, event):
        sender_id = event['sender_id']
        sender_username = event['sender_username']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'chat_request',
            'sender_id': sender_id,
            'sender_username': sender_username,
        }))
