from django.apps import AppConfig


class BusbookingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'busbooking'


    def ready(self):
        import busbooking.signals
