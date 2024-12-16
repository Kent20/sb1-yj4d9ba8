"""
Chat action views (sync, capture, release)
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import logging

from ...services import ChatService

logger = logging.getLogger(__name__)

@login_required
@require_http_methods(["POST"])
def sync_chats(request):
    """Sync chats from Telegram"""
    try:
        chat_service = ChatService()
        success = chat_service.sync_chats()
        
        if success:
            return JsonResponse({
                'status': 'success',
                'message': 'Чаты успешно синхронизированы'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Не удалось синхронизировать чаты'
            })
            
    except Exception as e:
        logger.error(f"Error syncing chats: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })

@login_required
@require_http_methods(["POST"])
def capture_chat(request):
    """Capture a chat for monitoring"""
    chat_id = request.POST.get('chat_id')
    if not chat_id:
        messages.error(request, 'Chat ID is required')
        return redirect('chat-list')
        
    try:
        chat_service = ChatService()
        success = chat_service.capture_chat(chat_id)
        
        if success:
            messages.success(request, f'Successfully captured chat {chat_id}')
        else:
            messages.error(request, f'Failed to capture chat {chat_id}')
            
    except Exception as e:
        logger.error(f"Error capturing chat: {str(e)}")
        messages.error(request, f'Error capturing chat: {str(e)}')
    
    return redirect('chat-list')

@login_required
@require_http_methods(["POST"]) 
def release_chat(request, chat_id):
    """Release a captured chat"""
    try:
        chat_service = ChatService()
        success = chat_service.release_chat(chat_id)
        
        if success:
            messages.success(request, 'Successfully released chat')
        else:
            messages.error(request, 'Failed to release chat')
            
    except Exception as e:
        logger.error(f"Error releasing chat: {str(e)}")
        messages.error(request, f'Error releasing chat: {str(e)}')
    
    return redirect('chat-list')