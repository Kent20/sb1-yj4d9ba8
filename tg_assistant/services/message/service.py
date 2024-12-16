"""
Service for handling messages
"""
from typing import List, Optional
from django.db import transaction
from ...models import Dialogue, CapturedChat
from ..base import BaseService
from .handlers import MessageHandler

class MessageService(BaseService):
    def __init__(self):
        super().__init__()
        self.handler = MessageHandler()

    async def process_message(
        self,
        chat: CapturedChat,
        message_text: str,
        sender_id: str,
        is_outgoing: bool = False
    ) -> Optional[str]:
        """Process a new message"""
        try:
            async with transaction.atomic():
                # Save message
                dialogue = await Dialogue.objects.acreate(
                    chat=chat,
                    message=message_text,
                    sender=sender_id,
                    is_outgoing=is_outgoing
                )

                if not chat.auto_reply or is_outgoing:
                    return None

                # Generate and send response
                return await self.handler.handle_message(dialogue)

        except Exception as e:
            self.logger.error(f"Error processing message: {str(e)}")
            return None