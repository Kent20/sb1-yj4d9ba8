"""
View for uploading dialogue data
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from ...forms import DialogueUploadForm
from ...services.dialogue import DialogueImportService
import json
import logging

logger = logging.getLogger(__name__)

@login_required
def upload_dialogues(request):
    """Handle dialogue data upload"""
    if request.method == 'POST':
        form = DialogueUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Load and parse JSON
                json_data = json.load(request.FILES['file'])
                
                # Process data
                import_service = DialogueImportService()
                if import_service.process_json_data(json_data):
                    messages.success(request, 'Dialogues uploaded successfully')
                    return redirect('dialogue-list')
                else:
                    messages.error(request, 'Error processing file')
                    
            except json.JSONDecodeError:
                messages.error(request, 'Invalid JSON file format')
            except Exception as e:
                logger.error(f"Error uploading dialogues: {str(e)}")
                messages.error(request, f'Error uploading dialogues: {str(e)}')
    else:
        form = DialogueUploadForm()
    
    return render(request, 'tg_assistant/dialogue/upload.html', {'form': form})