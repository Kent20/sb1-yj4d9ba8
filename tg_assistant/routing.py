"""
WebSocket URL configuration
"""
from django.urls import re_path
from .consumers import DialogueConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/dialogue/$', DialogueConsumer.as_asgi()),
]