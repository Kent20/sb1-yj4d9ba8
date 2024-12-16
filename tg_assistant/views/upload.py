"""
Views for file upload functionality
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from ..forms import DialogueUploadForm
from ..services.dialogue import DialogueImportService

@login_required
def upload_dialogues(request):
    if request.method == 'POST':
        form = DialogueUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                import_service = DialogueImportService()
                if import_service.process_json_data(request.FILES['file']):
                    messages.success(request, 'Диалоги успешно загружены')
                    return redirect('dialogue-list')
                else:
                    messages.error(request, 'Ошибка при обработке файла')
            except Exception as e:
                messages.error(request, f'Ошибка при загрузке: {str(e)}')
    else:
        form = DialogueUploadForm()
    
    return render(request, 'tg_assistant/dialogue/upload.html', {'form': form})