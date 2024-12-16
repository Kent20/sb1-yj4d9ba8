from telethon import TelegramClient, events
from telethon.tl.types import Message
import os
from dotenv import load_dotenv
from typing import List, Callable
import logging

class TelegramAssistant:
    def __init__(self):
        load_dotenv()
        
        self.api_id = os.getenv('API_ID')
        self.api_hash = os.getenv('API_HASH')
        self.phone = os.getenv('PHONE')
        self.session_name = os.getenv('SESSION_NAME')
        
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
        self.response_generator: Callable[[str], List[str]] = lambda x: []
        
    async def start(self):
        """Start the Telegram client"""
        await self.client.start(phone=self.phone)
        
        @self.client.on(events.NewMessage)
        async def handle_new_message(event: Message):
            # Don't mark as read
            await self.client.get_messages(event.chat_id, ids=[event.id], mark_read=False)
            
            if event.is_private:  # Only respond to private messages
                message_text = event.message.text
                suggested_responses = self.response_generator(message_text)
                
                # Log suggested responses (in production, you'd show these in UI)
                logging.info(f"Suggested responses for '{message_text}':")
                for response in suggested_responses:
                    logging.info(f"- {response}")
    
    def set_response_generator(self, generator: Callable[[str], List[str]]):
        """Set the function that generates response suggestions"""
        self.response_generator = generator
        
    async def stop(self):
        """Stop the Telegram client"""
        await self.client.disconnect()