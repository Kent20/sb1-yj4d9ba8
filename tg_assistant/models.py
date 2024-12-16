from django.db import models

class TelegramConfig(models.Model):
    api_id = models.CharField(max_length=255)
    api_hash = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    session_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)

class CapturedChat(models.Model):
    chat_id = models.CharField(max_length=255, unique=True)
    chat_title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    auto_reply = models.BooleanField(default=True)
    unread_count = models.IntegerField(default=0)
    last_message = models.TextField(null=True, blank=True)
    last_message_time = models.DateTimeField(null=True)

class Dialogue(models.Model):
    chat = models.ForeignKey(CapturedChat, on_delete=models.CASCADE)
    message = models.TextField()
    sender = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_outgoing = models.BooleanField(default=False)