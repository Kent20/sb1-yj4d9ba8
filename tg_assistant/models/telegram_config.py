from django.db import models

class TelegramConfig(models.Model):
    api_id = models.CharField(max_length=255, verbose_name="API ID")
    api_hash = models.CharField(max_length=255, verbose_name="API Hash")
    phone = models.CharField(max_length=20, verbose_name="Номер телефона")
    session_name = models.CharField(max_length=255, verbose_name="Имя сессии")
    is_active = models.BooleanField(default=False, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Настройки Telegram"
        verbose_name_plural = "Настройки Telegram"

    def __str__(self):
        return f"Telegram Config ({self.phone})"