from django.apps import AppConfig


class WebsocketConfig(AppConfig):
    # default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.websocket'
    
    def ready(self):
        from .signals import alojamientos_signals
        from .signals import habitaciones_signals
        from .signals import usuarios_signals