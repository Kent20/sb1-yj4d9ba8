"""
Core Telegram service for managing client connection and basic operations
"""
from telethon import TelegramClient, events
from django.conf import settings
from typing import Optional, List, Dict, Any
from ..models import TelegramConfig
import logging

logger = logging.getLogger(__name__)

class TelegramService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = None
        return cls._instance

    def start(self):
        """Start Telegram client"""
        if self.client and self.client.is_connected():
            return True

        try:
            config = TelegramConfig.objects.first()
            if not config:
                raise ValueError("Telegram configuration not found")

            self.client = TelegramClient(
                config.session_name,
                config.api_id,
                config.api_hash
            )
            
            self.client.start(phone=config.phone)
            config.is_active = True
            config.save()
            
            return True
        except Exception as e:
            logger.error(f"Error starting Telegram client: {str(e)}")
            return False

    def stop(self):
        """Stop Telegram client"""
        if self.client:
            self.client.disconnect()
            config = TelegramConfig.objects.first()
            if config:
                config.is_active = False
                config.save()

    async def get_chats(self) -> List[Dict[str, Any]]:
        """Get all user chats"""
        if not self.client:
            return []

        try:
            dialogs = await self.client.get_dialogs()
            return [
                {
                    'id': str(d.id),
                    'title': d.name,
                    'unread_count': d.unread_count,
                    'last_message': d.message.text if d.message else None,
                    'last_message_time': d.message.date if d.message else None
                }
                for d in dialogs
                if d.is_user  # Only get user chats
            ]
        except Exception as e:
            logger.error(f"Error getting chats: {str(e)}")
            return []

    async def send_message(self, chat_id: str, message: str) -> bool:
        """Send message to chat"""
        if not self.client:
            return False

        try:
            await self.client.send_message(chat_id, message)
            return True
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
            return False

    async def get_messages(self, chat_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get chat messages without marking as read"""
        if not self.client:
            return []

        try:
            messages = await self.client.get_messages(
                chat_id,
                limit=limit,
                mark_read=False
            )
            return [
                {
                    'id': m.id,
                    'text': m.text,
                    'sender': str(m.sender_id),
                    'timestamp': m.date,
                    'is_outgoing': m.out
                }
                for m in messages
            ]
        except Exception as e:
            logger.error(f"Error getting messages: {str(e)}")
            return []