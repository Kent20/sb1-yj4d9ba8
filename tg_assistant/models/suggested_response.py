from django.db import models
from .dialogue import Dialogue

class SuggestedResponse(models.Model):
    dialogue = models.ForeignKey(
        Dialogue,
        on_delete=models.CASCADE,
        related_name='suggested_responses',
        verbose_name="Диалог"
    )
    response_text = models.TextField(verbose_name="Текст ответа")
    confidence_score = models.FloatField(default=0.0, verbose_name="Уверенность")
    is_used = models.BooleanField(default=False, verbose_name="Использован")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")

    class Meta:
        verbose_name = "Предложенный ответ"
        verbose_name_plural = "Предложенные ответы"
        ordering = ['-confidence_score']

    def __str__(self):
        return f"Response to {self.dialogue.sender}: {self.response_text[:50]}..."