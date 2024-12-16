"""
Views for dialogue functionality
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, View
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

from ..models import Dialogue
from ..services.response.service import ResponseService

class DialogueListView(LoginRequiredMixin, ListView):
    model = Dialogue
    template_name = 'tg_assistant/dialogue/list.html'
    context_object_name = 'dialogues'
    paginate_by = 50

class ChatView(LoginRequiredMixin, View):
    template_name = 'tg_assistant/dialogue/chat.html'
    
    def get(self, request):
        messages = Dialogue.objects.all().order_by('timestamp')[:100]
        
        # Get initial suggestions
        response_service = ResponseService()
        suggestions = []
        if messages:
            suggestions = response_service.generate_responses(messages.last().message)
        
        return render(request, self.template_name, {
            'messages': messages,
            'suggestions': suggestions
        })

@login_required
@require_http_methods(["POST"])
def send_message(request):
    """Handle sending new messages"""
    try:
        data = json.loads(request.body)
        message = data.get('message')
        
        if message:
            dialogue = Dialogue.objects.create(
                message=message,
                sender=request.user.username,
                is_outgoing=True
            )
            return JsonResponse({'status': 'success'})
            
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
@require_http_methods(["GET"]) 
def get_suggestions(request):
    """Get AI suggestions for responses"""
    try:
        response_service = ResponseService()
        last_message = Dialogue.objects.last()
        
        suggestions = response_service.generate_responses(
            last_message.message if last_message else ""
        )
        return JsonResponse({'suggestions': suggestions})
        
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)