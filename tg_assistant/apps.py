from django.apps import AppConfig

class TgAssistantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tg_assistant'
    
    def ready(self):
        # Import signals
        from . import signals