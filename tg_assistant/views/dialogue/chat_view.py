"""
View for chat interface
"""
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...models import Dialogue
from ...services.response.service import ResponseService

class ChatView(LoginRequiredMixin, TemplateView):
    template_name = 'tg_assistant/dialogue/chat.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get messages with related data
        messages = (Dialogue.objects.select_related('chat')
                   .order_by('-timestamp')[:100])
        context['messages'] = reversed(messages) # Show in chronological order
        
        # Get initial suggestions
        if messages:
            service = ResponseService()
            context['suggestions'] = service.generate_responses(messages[0].message)
        
        return context