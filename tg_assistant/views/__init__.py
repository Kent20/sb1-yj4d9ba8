"""
Views package initialization
"""
from .dashboard import DashboardView
from .dialogue import DialogueListView, ChatView
from .chat import (
    ChatListView, ChatDetailView, CapturedChatListView,
    sync_chats, capture_chat, release_chat
)
from .telegram import TelegramConfigView
from .upload import upload_dialogues
from .api import generate_suggestions

__all__ = [
    'DashboardView',
    'DialogueListView',
    'ChatView',
    'ChatListView', 
    'ChatDetailView',
    'CapturedChatListView',
    'sync_chats',
    'capture_chat',
    'release_chat',
    'TelegramConfigView',
    'upload_dialogues',
    'generate_suggestions'
]