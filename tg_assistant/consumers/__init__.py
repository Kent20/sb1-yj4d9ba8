"""
WebSocket consumers package
"""
from .dialogue import DialogueConsumer
from .chat import ChatConsumer

__all__ = [
    'DialogueConsumer',
    'ChatConsumer'
]