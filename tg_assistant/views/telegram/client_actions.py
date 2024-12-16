"""
Views for managing Telegram client state
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from ...services import TelegramService
import threading
import logging

logger = logging.getLogger(__name__)

@login_required
def start_telegram_client(request):
    """Start the Telegram client"""
    try:
        service = TelegramService()
        thread = threading.Thread(target=service.start)
        thread.daemon = True
        thread.start()
        messages.success(request, 'Telegram client started successfully')
    except Exception as e:
        logger.error(f"Error starting Telegram client: {str(e)}")
        messages.error(request, f'Error starting Telegram client: {str(e)}')
    return redirect('telegram-config')

@login_required
def stop_telegram_client(request):
    """Stop the Telegram client"""
    try:
        service = TelegramService()
        service.stop()
        messages.success(request, 'Telegram client stopped successfully')
    except Exception as e:
        logger.error(f"Error stopping Telegram client: {str(e)}")
        messages.error(request, f'Error stopping Telegram client: {str(e)}')
    return redirect('telegram-config')