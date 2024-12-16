from django.db import models
from .captured_chat import CapturedChat

class Dialogue(models.Model):
    chat = models.ForeignKey(
        CapturedChat,
        on_delete=models.CASCADE,
        related_name='dialogues',
        verbose_name="Чат"
    )
    message = models.TextField(verbose_name="Сообщение")
    sender = models.CharField(max_length=255, verbose_name="Отправитель")
    timestamp = models.DateTimeField(verbose_name="Время")
    context = models.TextField(blank=True, verbose_name="Контекст")
    is_outgoing = models.BooleanField(default=False, verbose_name="Исходящее")

    class Meta:
        verbose_name = "Диалог"
        verbose_name_plural = "Диалоги"
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.sender}: {self.message[:50]}..."