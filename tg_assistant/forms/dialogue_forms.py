from django import forms

class DialogueUploadForm(forms.Form):
    file = forms.FileField(
        label='Выберите JSON файл с диалогами',
        help_text='Файл должен быть в правильном JSON формате'
    )