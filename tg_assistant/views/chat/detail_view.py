"""
View for displaying individual chat details
"""
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...models import CapturedChat

class ChatDetailView(LoginRequiredMixin, DetailView):
    model = CapturedChat
    template_name = 'tg_assistant/chat/detail.html'
    context_object_name = 'chat'