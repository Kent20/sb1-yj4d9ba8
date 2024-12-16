"""
Main dashboard view
"""
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...models import Dialogue, CapturedChat, SuggestedResponse
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tg_assistant/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get statistics
        active_chats = CapturedChat.objects.filter(is_active=True)
        unread_chats = active_chats.filter(unread_count__gt=0)
        recent_messages = Dialogue.objects.filter(
            timestamp__gte=timezone.now() - timedelta(days=7)
        )
        
        # Calculate response rate
        total_messages = recent_messages.count()
        auto_responses = SuggestedResponse.objects.filter(
            is_used=True,
            created_at__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        response_rate = (
            round((auto_responses / total_messages) * 100)
            if total_messages > 0
            else 0
        )
        
        context.update({
            'active_chats_count': active_chats.count(),
            'unread_chats_count': unread_chats.count(),
            'total_messages': total_messages,
            'response_rate': response_rate,
            'recent_dialogues': recent_messages.select_related('chat')[:10]
        })
        
        return context