from django.apps import AppConfig


class AyraConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'AYRA'
    
def ready(self):
    import AYRA.signals