"""
Views for Telegram configuration
"""
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from ..models import TelegramConfig
from ..forms import TelegramConfigForm

class TelegramConfigView(LoginRequiredMixin, UpdateView):
    model = TelegramConfig
    form_class = TelegramConfigForm
    template_name = 'tg_assistant/telegram_config.html'
    success_url = reverse_lazy('telegram-config')

    def get_object(self, queryset=None):
        obj, _ = TelegramConfig.objects.get_or_create(
            defaults={
                'api_id': '',
                'api_hash': '',
                'phone': '',
                'session_name': 'tg_session'
            }
        )
        return obj