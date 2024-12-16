from django.urls import re_path
from tg_assistant.consumers import DialogueConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/dialogue/$', DialogueConsumer.as_asgi()),
]