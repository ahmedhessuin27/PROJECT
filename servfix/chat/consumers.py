from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_id = None
        self.room_group_name = None

    async def connect(self):
        # Retrieve room ID from URL route parameters
        try:
            self.room_id = self.scope['url_route']['kwargs']['room_id']
        except KeyError:
            # Handle missing 'room_id' parameter
            # Close the connection or take appropriate action
            await self.close()
            return

        # Construct room group name using room ID
        self.room_group_name = f'chat_{self.room_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept connection
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        if text_data:
            try:
                text_data_json = json.loads(text_data)
                message = text_data_json['message']
            except json.JSONDecodeError:
                # Handle JSON decoding error
                # Log the error or take appropriate action
                return
            except KeyError:
                # Handle missing 'message' key in the JSON data
                # Log the error or take appropriate action
                return

            # Process the received message
            # For example, send the message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message
                }
            )
        else:
            # Handle empty message data
            # Log the error or take appropriate action
            return


    async def chat_message(self, event):
        # Receive message from room group
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
