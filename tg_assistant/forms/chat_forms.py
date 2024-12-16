from django import forms

class CaptureForm(forms.Form):
    chat_id = forms.CharField(
        label='ID чата',
        help_text='Введите ID Telegram чата для захвата'
    )