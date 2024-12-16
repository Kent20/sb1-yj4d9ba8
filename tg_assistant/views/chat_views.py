from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from ..models import CapturedChat
from ..forms import CaptureForm
from ..services import TelegramService, ChatService
import asyncio
import logging

logger = logging.getLogger(__name__)

class CapturedChatListView(LoginRequiredMixin, ListView):
    model = CapturedChat
    template_name = 'tg_assistant/captured_chats.html'
    context_object_name = 'chats'

    def get_queryset(self):
        """Only show chats with unread messages"""
        return CapturedChat.objects.filter(unread_count__gt=0).order_by('-last_message_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['auto_refresh'] = True
        return context

@login_required
@require_http_methods(["POST"])
def capture_chat(request):
    """Capture a chat for monitoring"""
    chat_id = request.POST.get('chat_id')
    if not chat_id:
        messages.error(request, 'Chat ID is required')
        return redirect('captured-chats')
        
    try:
        chat_service = ChatService()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(chat_service.capture_chat(chat_id))
        loop.close()
        
        if success:
            messages.success(request, f'Successfully captured chat {chat_id}')
        else:
            messages.error(request, f'Failed to capture chat {chat_id}')
            
    except Exception as e:
        logger.error(f"Error capturing chat: {str(e)}")
        messages.error(request, f'Error capturing chat: {str(e)}')
    
    return redirect('captured-chats')

@login_required
@require_http_methods(["POST"])
def release_chat(request, chat_id):
    """Release a captured chat"""
    try:
        chat = get_object_or_404(CapturedChat, id=chat_id)
        chat_service = ChatService()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(chat_service.release_chat(chat_id))
        loop.close()
        
        if success:
            messages.success(request, f'Successfully released chat {chat.chat_title}')
        else:
            messages.error(request, f'Failed to release chat {chat.chat_title}')
            
    except Exception as e:
        logger.error(f"Error releasing chat: {str(e)}")
        messages.error(request, f'Error releasing chat: {str(e)}')
    
    return redirect('captured-chats')

@login_required
def sync_chats(request):
    """Sync chats from Telegram"""
    try:
        service = TelegramService()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        chats = loop.run_until_complete(service.get_chats())
        loop.close()
        
        return JsonResponse({
            'status': 'success',
            'chats': [
                {
                    'id': chat.id,
                    'title': chat.chat_title,
                    'unread_count': chat.unread_count,
                    'last_message': chat.last_message
                }
                for chat in chats if chat.unread_count > 0
            ]
        })
    except Exception as e:
        logger.error(f"Error syncing chats: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })