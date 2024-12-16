from telethon import TelegramClient, events
from .models import TelegramConfig, CapturedChat, Dialogue
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import asyncio
import logging

logger = logging.getLogger(__name__)

class TelegramService:
    def __init__(self):
        self.config = TelegramConfig.objects.first()
        if not self.config:
            raise ValueError("Telegram configuration not found")
        
        self.client = TelegramClient(
            self.config.session_name,
            self.config.api_id,
            self.config.api_hash
        )
        
        # Initialize model
        self.model_name = "gpt2"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model.to(self.device)

    async def handle_new_message(self, event):
        # Don't mark as read
        await self.client.get_messages(event.chat_id, ids=[event.id], mark_read=False)
        
        chat = await CapturedChat.objects.filter(
            chat_id=str(event.chat_id),
            is_active=True
        ).afirst()
        
        if chat and not event.out:
            message = event.message.text
            
            # Save dialogue
            dialogue = await Dialogue.objects.acreate(
                chat=chat,
                message=message,
                sender=str(event.sender_id),
                is_outgoing=False
            )
            
            if chat.auto_reply:
                # Generate response
                response = await self.generate_response(message)
                
                # Send response
                await event.respond(response)
                
                # Save response
                await Dialogue.objects.acreate(
                    chat=chat,
                    message=response,
                    sender="Assistant",
                    is_outgoing=True
                )

    async def generate_response(self, message):
        inputs = self.tokenizer.encode(message, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            inputs, 
            max_length=100,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.eos_token_id
        )
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response

    async def capture_chat(self, chat_id: int):
        """Capture chat for monitoring"""
        try:
            chat = await self.client.get_entity(chat_id)
            await CapturedChat.objects.acreate(
                chat_id=str(chat_id),
                chat_title=getattr(chat, 'title', str(chat_id)),
                is_active=True,
                auto_reply=True
            )
            return True
        except Exception as e:
            logger.error(f"Error capturing chat: {e}")
            return False

    def start(self):
        """Start the client"""
        self.client.start(phone=self.config.phone)
        
        @self.client.on(events.NewMessage)
        async def message_handler(event):
            await self.handle_new_message(event)
        
        self.config.is_active = True
        self.config.save()
        
        self.client.run_until_disconnected()