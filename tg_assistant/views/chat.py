"""
Views for chat management
"""
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import CapturedChat

class ChatListView(LoginRequiredMixin, ListView):
    model = CapturedChat
    template_name = 'tg_assistant/chat/list.html'
    context_object_name = 'chats'

class ChatDetailView(LoginRequiredMixin, DetailView):
    model = CapturedChat
    template_name = 'tg_assistant/chat/detail.html'
    context_object_name = 'chat'

class CapturedChatListView(LoginRequiredMixin, ListView):
    model = CapturedChat
    template_name = 'tg_assistant/chat/captured_list.html'
    context_object_name = 'chats'
    
    def get_queryset(self):
        return CapturedChat.objects.filter(is_active=True)