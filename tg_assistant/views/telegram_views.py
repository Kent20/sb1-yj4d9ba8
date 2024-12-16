from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from ..models import TelegramConfig
from ..forms import TelegramConfigForm
from ..services import TelegramService
import threading

class TelegramConfigView(LoginRequiredMixin, UpdateView):
    model = TelegramConfig
    form_class = TelegramConfigForm
    template_name = 'tg_assistant/telegram_config.html'
    success_url = reverse_lazy('telegram-config')

    def get_object(self, queryset=None):
        obj, created = TelegramConfig.objects.get_or_create(
            defaults={
                'api_id': '',
                'api_hash': '',
                'phone': '',
                'session_name': 'tg_session'
            }
        )
        return obj

@login_required
def start_telegram_client(request):
    service = TelegramService()
    thread = threading.Thread(target=service.start)
    thread.daemon = True
    thread.start()
    messages.success(request, 'Telegram client started successfully')
    return redirect('telegram-config')