"""
Service for importing dialogues from Telegram JSON export
"""
from typing import Dict
from django.db import transaction
from django.utils import timezone
import json
import logging

from ...models import CapturedChat, Dialogue
from .validators import DialogueValidator
from .message_parser import MessageParser
from .chat_mapper import ChatMapper

logger = logging.getLogger(__name__)

class DialogueImportService:
    def __init__(self):
        self.validator = DialogueValidator()
        self.parser = MessageParser()
        self.mapper = ChatMapper()

    def process_json_data(self, file) -> bool:
        """Process Telegram export JSON data"""
        try:
            # Parse JSON file
            data = json.load(file)
            
            # Validate structure
            if not self.validator.validate_json_structure(data):
                logger.error("Invalid JSON structure")
                return False
                
            with transaction.atomic():
                # Create or update chat
                chat = CapturedChat.objects.update_or_create(
                    chat_id=str(data.get('id', '')),
                    defaults={
                        'chat_title': data.get('name', 'Unknown Chat'),
                        'chat_type': self.mapper.map_chat_type(data.get('type')),
                        'is_active': True
                    }
                )[0]

                # Import messages chronologically
                messages = sorted(
                    data.get('messages', []),
                    key=lambda x: int(x.get('date_unixtime', 0))
                )
                
                for msg in messages:
                    if msg.get('type') != 'message':
                        continue
                        
                    # Extract message text
                    text = self.parser.extract_message_text(msg)
                    if not text:
                        continue

                    # Create dialogue entry with timezone-aware datetime
                    timestamp = self.parser.parse_timestamp(msg.get('date'))
                    if timestamp.tzinfo is None:
                        timestamp = timezone.make_aware(timestamp)

                    Dialogue.objects.create(
                        chat=chat,
                        message=text,
                        sender=msg.get('from', ''),
                        timestamp=timestamp,
                        is_outgoing=bool(msg.get('from_id') == msg.get('saved_from'))
                    )
                    
            return True
            
        except Exception as e:
            logger.error(f"Error importing dialogues: {str(e)}")
            return False