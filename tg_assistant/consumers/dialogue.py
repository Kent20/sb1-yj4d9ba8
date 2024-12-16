"""
WebSocket consumer for dialogue chat
"""
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
import json

from ..models import Dialogue
from ..services.response.service import ResponseService

class DialogueConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        """Handle WebSocket connection"""
        await self.channel_layer.group_add('dialogue_chat', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        await self.channel_layer.group_discard('dialogue_chat', self.channel_name)

    async def receive(self, text_data):
        """Handle received messages"""
        data = json.loads(text_data)
        message = data['message']
        
        # Save message
        dialogue = await self.save_message(message)
        
        # Generate suggestions
        response_service = ResponseService()
        suggestions = response_service.generate_responses(message)
        
        # Broadcast message and suggestions
        await self.channel_layer.group_send(
            'dialogue_chat',
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