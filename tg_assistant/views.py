from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from .models import CapturedChat, Dialogue
from .services import TelegramService
import json

@login_required
def capture_chat(request):
    if request.method == 'POST':
        chat_id = request.POST.get('chat_id')
        if chat_id:
            service = TelegramService()
            success = await service.capture_chat(int(chat_id))
            if success:
                messages.success(request, 'Chat captured successfully')
            else:
                messages.error(request, 'Failed to capture chat')
    return redirect('chat-list')

class ChatListView(ListView):
    model = CapturedChat
    template_name = 'tg_assistant/chat_list.html'
    context_object_name = 'chats'

@login_required
def upload_dialogues(request):
    if request.method == 'POST':
        try:
            dialogues = json.load(request.FILES['file'])
            for dialogue in dialogues:
                Dialogue.objects.create(
                    message=dialogue['message'],
                    sender=dialogue['sender'],
                    timestamp=dialogue['timestamp']
                )
            messages.success(request, 'Dialogues uploaded successfully')
        except Exception as e:
            messages.error(request, f'Error uploading dialogues: {e}')
    return render(request, 'tg_assistant/upload.html')