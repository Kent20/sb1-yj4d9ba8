from ..models import Dialogue, SuggestedResponse
from .response_service import ResponseService
from asgiref.sync import sync_to_async
import logging

logger = logging.getLogger(__name__)

class DialogueService:
    def __init__(self):
        self.response_service = ResponseService()

    async def process_message(self, message_text, sender_id, timestamp, chat, event):
        dialogue = await sync_to_async(Dialogue.objects.create)(
            message=message_text,
            sender=str(sender_id),
            timestamp=timestamp
        )
        
        responses = self.response_service.generate_responses(message_text)
        
        if chat.auto_reply and responses:
            best_response = responses[0]
            
            await sync_to_async(SuggestedResponse.objects.create)(
                dialogue=dialogue,
                response_text=best_response,
                confidence_score=0.9,
                is_used=True
            )
            
            await event.respond(best_response)
            logger.info(f"Sent auto-reply to chat {chat.chat_title}: {best_response[:50]}...")
        
        for response in responses[1:]:
            await sync_to_async(SuggestedResponse.objects.create)(
                dialogue=dialogue,
                response_text=response,
                confidence_score=0.8
            )
        
        logger.info(f"Processed message in {chat.chat_title}: {message_text[:50]}...")