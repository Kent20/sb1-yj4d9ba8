"""
WebSocket consumers for real-time chat functionality
"""
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
import json

from .models import Dialogue
from .services.response.service import ResponseService

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_room'
        self.response_service = ResponseService()

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
        """Handle received messages"""
        data = json.loads(text_data)
        message = data['message']
        
        # Save message to database
        dialogue = await self.save_message(message)
        
        # Generate response suggestions
        suggestions = await self.response_service.generate_responses(message)
        
        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': dialogue.sender,
                'timestamp': dialogue.timestamp.isoformat(),
                'is_outgoing': dialogue.is_outgoing,
                'suggestions': suggestions
            }
        )

    async def chat_message(self, event):
        """Send message to WebSocket"""
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message(self, message):
        """Save message to database"""
        return Dialogue.objects.create(
            message=message,
            sender=self.scope['user'].username,
            timestamp=timezone.now(),
            is_outgoing=True
        )