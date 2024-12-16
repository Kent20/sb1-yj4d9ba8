"""
Message handling logic
"""
from typing import Optional
from django.db import transaction
from ...models import Dialogue, SuggestedResponse
from ..response import ResponseService

class MessageHandler:
    def __init__(self):
        self.response_service = ResponseService()

    async def handle_message(self, dialogue: Dialogue) -> Optional[str]:
        """Handle a new message and generate response"""
        try:
            # Get context and generate responses
            context = await self._get_chat_context(dialogue.chat_id)
            responses = await self.response_service.generate_responses(
                dialogue.message,
                context=context
            )

            if not responses:
                return None

            # Save and use best response
            async with transaction.atomic():
                await SuggestedResponse.objects.acreate(
                    dialogue=dialogue,
                    response_text=responses[0],
                    confidence_score=0.9,
                    is_used=True
                )

                # Save other suggestions
                for response in responses[1:]:
                    await SuggestedResponse.objects.acreate(
                        dialogue=dialogue,
                        response_text=response,
                        confidence_score=0.7
                    )

            return responses[0]

        except Exception as e:
            self.logger.error(f"Error handling message: {str(e)}")
            return None

    async def _get_chat_context(self, chat_id: int, limit: int = 5) -> list:
        """Get recent messages for context"""
        messages = await Dialogue.objects.filter(
            chat_id=chat_id
        ).order_by('-timestamp')[:limit]
        
        return [msg.message async for msg in messages]