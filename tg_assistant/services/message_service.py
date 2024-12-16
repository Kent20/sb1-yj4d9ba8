"""
Service for handling messages and responses
"""
from typing import List
from django.db import transaction
from .base import BaseService
from .response_service import ResponseService
from ..models import Dialogue, SuggestedResponse, CapturedChat

class MessageService(BaseService):
    def __init__(self):
        super().__init__()
        self.response = ResponseService()

    async def handle_new_message(self, chat: CapturedChat, message_text: str, sender_id: str):
        """Handle a new message in a chat"""
        async with transaction.atomic():
            # Save message
            message = await Dialogue.objects.acreate(
                chat=chat,
                message=message_text,
                sender=sender_id,
                is_outgoing=False
            )

            if not chat.auto_reply:
                return

            # Get context and generate responses
            context = await self._get_chat_context(chat)
            responses = await self.response.generate_responses(
                message_text,
                context=context
            )

            if not responses:
                return

            # Save and use best response
            await SuggestedResponse.objects.acreate(
                dialogue=message,
                response_text=responses[0],
                confidence_score=0.9,
                is_used=True
            )

            # Save other suggestions
            for response in responses[1:]:
                await SuggestedResponse.objects.acreate(
                    dialogue=message,
                    response_text=response,
                    confidence_score=0.7
                )

            return responses[0]

    async def _get_chat_context(self, chat: CapturedChat, limit: int = 5) -> List[str]:
        """Get recent messages for context"""
        messages = await Dialogue.objects.filter(
            chat=chat
        ).order_by('-timestamp')[:limit]
        
        return [msg.message async for msg in messages]