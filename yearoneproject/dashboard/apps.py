from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

    def ready(self):
     # import your signal file in here if the app is ready
       # from . import signals
        import dashboard.signals
