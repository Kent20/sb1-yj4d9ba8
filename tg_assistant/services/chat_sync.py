"""
Service for synchronizing chat data with Telegram
"""
from typing import List, Dict, Any
from asgiref.sync import sync_to_async
from django.db import transaction
from ..models import CapturedChat
import logging

logger = logging.getLogger(__name__)

class ChatSyncService:
    @staticmethod
    async def sync_chats(chats_data: List[Dict[str, Any]]) -> bool:
        """
        Synchronize chats with database
        
        Args:
            chats_data: List of chat information from Telegram
            
        Returns:
            bool: True if sync successful, False otherwise
        """
        try:
            async with transaction.atomic():
                for chat_info in chats_data:
                    await CapturedChat.objects.aupdate_or_create(
                        chat_id=chat_info['id'],
                        defaults={
                            'chat_title': chat_info['title'],
                            'chat_type': chat_info.get('type', 'unknown'),
                            'unread_count': chat_info.get('unread_count', 0),
                            'last_message_text': chat_info.get('last_message'),
                            'last_message_time': chat_info.get('last_message_time')
                        }
                    )
            return True
            
        except Exception as e:
            logger.error(f"Error syncing chats: {str(e)}")
            return False

    @staticmethod
    async def get_unread_chats() -> List[Dict[str, Any]]:
        """Get all chats with unread messages"""
        try:
            chats = await sync_to_async(list)(
                CapturedChat.objects.filter(unread_count__gt=0)
                .order_by('-last_message_time')
            )
            
            return [
                {
                    'id': chat.id,
                    'title': chat.chat_title,
                    'type': chat.get_chat_type_display(),
                    'unread_count': chat.unread_count,
                    'last_message': chat.last_message_text,
                    'is_active': chat.is_active
                }
                for chat in chats
            ]
            
        except Exception as e:
            logger.error(f"Error getting unread chats: {str(e)}")
            return []