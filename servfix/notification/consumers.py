from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import ChatMessages

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_authenticated:
            if hasattr(self.scope["user"], "providerprofile"):
                self.room_group_name = f'provider_{self.scope["user"].providerprofile.id}'
            else:
                self.room_group_name = f'user_{self.scope["user"].id}'

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
        text_data_json = json.loads(text_data)
        message_content = text_data_json['content']
        message = ChatMessages.objects.create(content=message_content,sender=self.scope['user'])
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))