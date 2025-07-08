from django.apps import AppConfig


class BoardingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'boarding'
    verbose_name = 'Boarding Management'
    
    def ready(self):
        # Import signals when app is ready
        try:
            import boarding.signals
        except ImportError:
            pass
