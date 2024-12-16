from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Dialogue
from ..forms import DialogueUploadForm
import json

class DialogueListView(LoginRequiredMixin, ListView):
    model = Dialogue
    template_name = 'tg_assistant/dialogue_list.html'
    context_object_name = 'dialogues'
    paginate_by = 50

@login_required
def upload_dialogues(request):
    if request.method == 'POST':
        form = DialogueUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                dialogues = json.load(request.FILES['file'])
                for dialogue_data in dialogues:
                    Dialogue.objects.create(
                        message=dialogue_data['message'],
                        sender=dialogue_data['sender'],
                        timestamp=dialogue_data['timestamp'],
                        context=dialogue_data.get('context', '')
                    )
                messages.success(request, 'Dialogues uploaded successfully')
                return redirect('dialogue-list')
            except Exception as e:
                messages.error(request, f'Error uploading dialogues: {str(e)}')
    else:
        form = DialogueUploadForm()
    
    return render(request, 'tg_assistant/upload_dialogues.html', {'form': form})