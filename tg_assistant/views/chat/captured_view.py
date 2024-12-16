"""
View for displaying captured chats
"""
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...models import CapturedChat

class CapturedChatListView(LoginRequiredMixin, ListView):
    model = CapturedChat
    template_name = 'tg_assistant/chat/captured_list.html'
    context_object_name = 'chats'
    
    def get_queryset(self):
        return CapturedChat.objects.filter(is_active=True).order_by('-last_message_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auto_refresh'] = True
        return context