from django.contrib import admin
from .models import TelegramConfig, CapturedChat, Dialogue, SuggestedResponse

@admin.register(TelegramConfig)
class TelegramConfigAdmin(admin.ModelAdmin):
    list_display = ('phone', 'is_active', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('phone',)

@admin.register(CapturedChat)
class CapturedChatAdmin(admin.ModelAdmin):
    list_display = ('chat_title', 'chat_id', 'is_active', 'auto_reply', 'created_at')
    list_filter = ('is_active', 'auto_reply')
    search_fields = ('chat_title', 'chat_id')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Dialogue)
class DialogueAdmin(admin.ModelAdmin):
    list_display = ('sender', 'message', 'timestamp', 'chat')
    list_filter = ('chat', 'timestamp')
    search_fields = ('message', 'sender')
    readonly_fields = ('timestamp',)

@admin.register(SuggestedResponse)
class SuggestedResponseAdmin(admin.ModelAdmin):
    list_display = ('dialogue', 'response_text', 'confidence_score', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('response_text',)
    readonly_fields = ('created_at',)