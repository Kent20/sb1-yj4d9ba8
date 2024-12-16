"""
Service for managing chat operations
"""
from typing import Optional, List, Dict, Any
from django.db import transaction
from django.utils import timezone
from asgiref.sync import sync_to_async
from ..models import CapturedChat, Dialogue
from .telegram_service import TelegramService
import logging

logger = logging.getLogger(__name__)

class ChatService:
    def __init__(self):
        self.telegram = TelegramService()

    def sync_chats(self) -> bool:
        """Sync chats with Telegram"""
        try:
            # Get chats from Telegram
            chats = self.telegram.get_chats()
            
            with transaction.atomic():
                for chat_info in chats:
                    CapturedChat.objects.update_or_create(
                        chat_id=chat_info['id'],
                        defaults={
                            'chat_title': chat_info['title'],
                            'unread_count': chat_info.get('unread_count', 0),
                            'last_message_text': chat_info.get('last_message'),
                            'last_message_time': chat_info.get('last_message_time') or timezone.now()
                        }
                    )
            return True
            
        except Exception as e:
            logger.error(f"Error syncing chats: {str(e)}")
            return False