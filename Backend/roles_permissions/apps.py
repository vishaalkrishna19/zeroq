from django.apps import AppConfig


class RolesPermissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'roles_permissions'
    verbose_name = 'Roles and Permissions'
    
    def ready(self):
        # Import signals when app is ready
        try:
            import roles_permissions.signals
        except ImportError:
            pass