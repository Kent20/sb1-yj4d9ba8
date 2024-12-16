"""
Message parsing utilities for dialogue import
"""
from typing import Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class MessageParser:
    def extract_message_text(self, msg_data: Dict) -> str:
        """Extract message text preserving formatting"""
        try:
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

        except Exception as e:
            logger.error(f"Error extracting message text: {str(e)}")
            return ''

    def parse_timestamp(self, date_str: Optional[str]) -> datetime:
        """Parse Telegram timestamp format"""
        if not date_str:
            return datetime.now()
            
        try:
            return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
        except (ValueError, TypeError) as e:
            logger.error(f"Error parsing timestamp {date_str}: {str(e)}")
            return datetime.now()