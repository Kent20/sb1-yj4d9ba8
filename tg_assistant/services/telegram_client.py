from telethon import TelegramClient, events
from django.conf import settings
from ..models import TelegramConfig, CapturedChat
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class TelegramClientService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = None
        return cls._instance

    async def initialize(self):
        """Initialize Telegram client"""
        if not self.client:
            config = await TelegramConfig.objects.afirst()
            if not config:
                raise ValueError("Telegram configuration not found")

            self.client = TelegramClient(
                config.session_name,
                config.api_id,
                config.api_hash
            )
            await self.client.connect()

            if not await self.client.is_user_authorized():
                await self.client.sign_in(phone=config.phone)

    async def get_all_chats(self) -> List[Dict[str, Any]]:
        """Get all available chats"""
        await self.initialize()
        
        dialogs = await self.client.get_dialogs()
        chats = []
        
        for dialog in dialogs:
            if dialog.is_user:  # Only get user chats
                chat_info = {
                    'id': str(dialog.id),
                    'title': dialog.name,
                    'unread_count': dialog.unread_count,
                    'last_message': dialog.message.text if dialog.message else None,
                    'last_message_time': dialog.message.date if dialog.message else None
                }
                chats.append(chat_info)
                
                # Update or create chat in database
                await CapturedChat.objects.aupdate_or_create(
                    chat_id=chat_info['id'],
                    defaults={
                        'chat_title': chat_info['title'],
                        'unread_count': chat_info['unread_count'],
                        'last_message': chat_info['last_message'],
                        'last_message_time': chat_info['last_message_time']
                    }
                )
        
        return chats