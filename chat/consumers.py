import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from accounts.models import CustomUser
from .models import Message, Room


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = ''
        self.room_id = ''

    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'room_{self.room_id}'

        # Join room group.
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group.
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket.
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']

        # Save message to database.
        await self.save_message(username, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                'type': 'room_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from room group.
    async def room_message(self, event):
        message = event['message']
        username = event['username']

        # Save message to database.
        # await self.save_message(message)

        # Send message to WebSocket.
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    # Create message object in database.
    @database_sync_to_async
    def save_message(self, username, message):
        Message.objects.create(
            room=Room.objects.get(id=self.room_id),  # Room object.
            user=CustomUser.objects.get(username=username),  # User object.
            text=message,  # Message text content.
        )