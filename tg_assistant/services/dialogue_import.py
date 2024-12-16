"""
Service for importing dialogues from Telegram JSON export
"""
from datetime import datetime
from typing import Dict, List, Optional
from django.db import transaction
from ..models import CapturedChat, Dialogue
import logging

logger = logging.getLogger(__name__)

class DialogueImportService:
    def process_json_data(self, data: Dict) -> bool:
        """Process Telegram export JSON data"""
        try:
            if not self._validate_json_structure(data):
                logger.error("Invalid JSON structure")
                return False
                
            with transaction.atomic():
                chats = data.get('chats', {}).get('list', [])
                for chat_data in chats:
                    self._import_chat(chat_data)
                    
            return True
            
        except Exception as e:
            logger.error(f"Error importing dialogues: {str(e)}")
            return False

    def _import_chat(self, chat_data: Dict) -> Optional[CapturedChat]:
        """Import a single chat with all messages"""
        try:
            chat_id = str(chat_data.get('id', ''))
            if not chat_id:
                return None

            # Create or update chat
            chat = CapturedChat.objects.update_or_create(
                chat_id=chat_id,
                defaults={
                    'chat_title': chat_data.get('name', chat_data.get('type', 'Unknown Chat')),
                    'chat_type': self._map_chat_type(chat_data.get('type')),
                    'is_active': True  # Activate imported chats by default
                }
            )[0]

            # Import all messages in chronological order
            messages = sorted(
                chat_data.get('messages', []),
                key=lambda x: x.get('date_unixtime', 0)
            )
            
            for msg in messages:
                self._import_message(chat, msg)

            return chat

        except Exception as e:
            logger.error(f"Error importing chat {chat_data.get('id')}: {str(e)}")
            return None

    def _import_message(self, chat: CapturedChat, msg_data: Dict) -> Optional[Dialogue]:
        """Import a single message preserving conversation flow"""
        try:
            # Get message text
            text = self._extract_message_text(msg_data)
            if not text:
                return None

            # Determine message direction
            sender = msg_data.get('from', '')
            is_outgoing = bool(msg_data.get('from_id') == msg_data.get('saved_from'))

            # Create dialogue entry
            return Dialogue.objects.create(
                chat=chat,
                message=text,
                sender=sender,
                timestamp=self._parse_timestamp(msg_data.get('date')),
                is_outgoing=is_outgoing
            )

        except Exception as e:
            logger.error(f"Error importing message: {str(e)}")
            return None

    def _extract_message_text(self, msg_data: Dict) -> str:
        """Extract message text preserving formatting"""
        # Handle simple text
        if isinstance(msg_data.get('text'), str):
            return msg_data['text']

        # Handle structured text with entities
        if isinstance(msg_data.get('text'), list):
            return ''.join(
                item.get('text', str(item))
                for item in msg_data['text']
            )

        # Handle text entities
        if msg_data.get('text_entities'):
            return ''.join(
                entity.get('text', '')
                for entity in msg_data['text_entities']
            )

        return ''