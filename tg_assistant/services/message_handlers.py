"""
Message handling service
"""
from typing import Optional
from asgiref.sync import sync_to_async
from django.db import transaction
from ..models import CapturedChat, Dialogue
from .response_service import ResponseService
import logging

logger = logging.getLogger(__name__)

async def handle_new_message(event, client) -> None:
    """Handle new message without marking as read"""
    try:
        # Get message without marking as read
        message = await client.get_messages(
            event.chat_id,
            ids=[event.id],
            mark_read=False
        )
        
        chat = await get_active_chat(str(event.chat_id))
        if not chat:
            return
            
        # Save message and generate response
        dialogue = await save_message(chat, message)
        
        if chat.auto_reply:
            response_service = ResponseService()
            responses = await response_service.generate_responses(message.text)
            
            if responses:
                await client.send_message(event.chat_id, responses[0])
            
    except Exception as e:
        logger.error(f"Error handling message: {str(e)}")

@sync_to_async
def get_active_chat(chat_id: str) -> Optional[CapturedChat]:
    """Get active chat by ID"""
    return CapturedChat.objects.filter(
        chat_id=chat_id,
        is_active=True
    ).first()

@sync_to_async
def save_message(chat: CapturedChat, message) -> Dialogue:
    """Save message to database"""
    with transaction.atomic():
        return Dialogue.objects.create(
            chat=chat,
            message=message.text,
            sender=str(message.sender_id),
            timestamp=message.date,
            is_outgoing=message.out
        )