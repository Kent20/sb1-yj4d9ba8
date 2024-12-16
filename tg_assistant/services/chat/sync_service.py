"""
Service for syncing chats with Telegram
"""
from typing import List, Dict, Any
from django.db import transaction
from asgiref.sync import sync_to_async
from ...models import CapturedChat
import logging

logger = logging.getLogger(__name__)

class ChatSyncService:
    async def get_unread_chats(self) -> List[Dict[str, Any]]:
        """Get all chats with unread messages"""
        try:
            chats = await sync_to_async(list)(
                CapturedChat.objects.filter(unread_count__gt=0)
                .order_by('-last_message_time')
            )
            
            return [
                {
                    'id': chat.chat_id,
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

    async def sync_chats(self, chats_data: List[Dict[str, Any]]) -> bool:
        """Sync chats with database"""
        try:
            async with transaction.atomic():
                for chat_info in chats_data:
                    await sync_to_async(CapturedChat.objects.update_or_create)(
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