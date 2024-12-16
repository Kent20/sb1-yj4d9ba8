"""
URL configuration for tg_assistant app
"""
from django.urls import path
from . import views

urlpatterns = [
    # Main views
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('dialogues/', views.DialogueListView.as_view(), name='dialogue-list'),
    path('dialogues/chat/', views.ChatView.as_view(), name='dialogue-chat'),
    path('dialogues/upload/', views.upload_dialogues, name='upload-dialogues'),
    
    # Chat management
    path('chats/', views.ChatListView.as_view(), name='chat-list'),
    path('chats/<int:pk>/', views.ChatDetailView.as_view(), name='chat-detail'),
    path('chats/captured/', views.CapturedChatListView.as_view(), name='captured-chats'),
    path('chats/sync/', views.sync_chats, name='sync-chats'),
    path('chats/<int:chat_id>/release/', views.release_chat, name='release-chat'),
    path('chats/capture/', views.capture_chat, name='capture-chat'),
    
    # Telegram configuration
    path('telegram/config/', views.TelegramConfigView.as_view(), name='telegram-config'),
    
    # API endpoints
    path('api/suggestions/', views.generate_suggestions, name='generate-suggestions'),
]