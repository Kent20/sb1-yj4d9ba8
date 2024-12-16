"""
View for displaying chat list
"""
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...models import CapturedChat

class ChatListView(LoginRequiredMixin, ListView):
    model = CapturedChat
    template_name = 'tg_assistant/chat/list.html'
    context_object_name = 'chats'
    
    def get_queryset(self):
        return CapturedChat.objects.filter(unread_count__gt=0).order_by('-last_message_time')