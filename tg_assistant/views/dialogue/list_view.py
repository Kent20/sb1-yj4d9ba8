"""
View for displaying dialogue list
"""
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from ...models import Dialogue

class DialogueListView(LoginRequiredMixin, ListView):
    model = Dialogue
    template_name = 'tg_assistant/dialogue_list.html'
    context_object_name = 'dialogues'
    paginate_by = 50