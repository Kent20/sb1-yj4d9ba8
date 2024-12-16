from django.shortcuts import render, redirect
from django.contrib import messages
from ..forms import DialogueUploadForm
from ..models import Dialogue, CapturedChat
import json
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def upload_dialogues(request):
    if request.method == 'POST':
        form = DialogueUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                data = json.load(request.FILES['file'])
                if 'chats' in data and 'list' in data['chats']:
                    chats = data['chats']['list']
                    for chat in chats:
                        # Создаем или получаем чат
                        chat_obj, _ = CapturedChat.objects.get_or_create(
                            chat_id=str(chat.get('id', '')),
                            defaults={
                                'chat_title': chat.get('type', 'Unknown Chat'),
                                'is_active': True
                            }
                        )
                        
                        # Обрабатываем сообщения
                        for msg in chat.get('messages', []):
                            try:
                                timestamp = datetime.strptime(
                                    msg['date'],
                                    "%Y-%m-%dT%H:%M:%S"
                                )
                                
                                Dialogue.objects.create(
                                    chat=chat_obj,
                                    message=msg.get('text', ''),
                                    sender=msg.get('from', ''),
                                    timestamp=timestamp,
                                    context=msg.get('context', '')
                                )
                            except (KeyError, ValueError) as e:
                                continue
                                
                    messages.success(request, 'Диалоги успешно загружены')
                    return redirect('dialogue-list')
                else:
                    messages.error(request, 'Неверный формат JSON файла')
            except json.JSONDecodeError:
                messages.error(request, 'Ошибка при разборе JSON файла')
            except Exception as e:
                messages.error(request, f'Ошибка при загрузке диалогов: {str(e)}')
    else:
        form = DialogueUploadForm()
    
    return render(request, 'tg_assistant/upload_dialogues.html', {'form': form})