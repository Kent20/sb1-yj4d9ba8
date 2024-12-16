"""
Model for captured Telegram chats
"""
from django.db import models

class CapturedChat(models.Model):
    CHAT_TYPES = [
        ('user', 'Личный чат'),
        ('group', 'Группа'),
        ('channel', 'Канал'),
        ('unknown', 'Неизвестно')
    ]

    chat_id = models.CharField(max_length=255, unique=True, verbose_name="ID чата")
    chat_title = models.CharField(max_length=255, verbose_name="Название чата")
    chat_type = models.CharField(
        max_length=20,
        choices=CHAT_TYPES,
        default='unknown',
        verbose_name="Тип чата"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    auto_reply = models.BooleanField(default=True, verbose_name="Автоответ")
    unread_count = models.IntegerField(default=0, verbose_name="Непрочитанные")
    last_message_text = models.TextField(blank=True, null=True, verbose_name="Последнее сообщение")
    last_message_time = models.DateTimeField(null=True, blank=True, verbose_name="Время последнего сообщения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Обновлено")

    class Meta:
        verbose_name = "Захваченный чат"
        verbose_name_plural = "Захваченные чаты"
        ordering = ['-last_message_time', '-created_at']

    def __str__(self):
        return f"{self.chat_title} ({self.get_chat_type_display()})"