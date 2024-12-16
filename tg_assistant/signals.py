from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TelegramConfig
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=TelegramConfig)
def handle_telegram_config_save(sender, instance, created, **kwargs):
    """Handle TelegramConfig changes"""
    if created:
        logger.info(f"New Telegram configuration created for {instance.phone}")
    else:
        logger.info(f"Telegram configuration updated for {instance.phone}")