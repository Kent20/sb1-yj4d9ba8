from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import Dialogue, CapturedChat, SuggestedResponse
from django.db.models import Count

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tg_assistant/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            # Безопасное получение статистики
            active_chats = CapturedChat.objects.filter(is_active=True)
            total_dialogues = Dialogue.objects.all()
            total_responses = SuggestedResponse.objects.filter(is_used=True)
            
            context.update({
                'active_chats_count': active_chats.count() if active_chats.exists() else 0,
                'total_dialogues': total_dialogues.count() if total_dialogues.exists() else 0,
                'response_rate': 0,
                'recent_dialogues': []
            })
            
            if context['total_dialogues'] > 0:
                response_count = total_responses.count() if total_responses.exists() else 0
                context['response_rate'] = round((response_count / context['total_dialogues']) * 100)
                
            if total_dialogues.exists():
                context['recent_dialogues'] = (
                    Dialogue.objects.select_related('chat')
                    .order_by('-timestamp')[:10]
                )
                
        except Exception:
            context.update({
                'active_chats_count': 0,
                'total_dialogues': 0,
                'response_rate': 0,
                'recent_dialogues': []
            })
        
        return context