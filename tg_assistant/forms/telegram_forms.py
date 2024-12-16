from django import forms
from ..models import TelegramConfig

class TelegramConfigForm(forms.ModelForm):
    class Meta:
        model = TelegramConfig
        fields = ['api_id', 'api_hash', 'phone', 'session_name']
        widgets = {
            'api_hash': forms.PasswordInput(),
        }

class AuthCodeForm(forms.Form):
    code = forms.CharField(
        label='Код подтверждения',
        max_length=10,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите код из Telegram'
        })
    )

class CloudPasswordForm(forms.Form):
    password = forms.CharField(
        label='Облачный пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите ваш облачный пароль'
        })
    )