from django.apps import AppConfig


class ChannleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'channle'

    def ready(self):
        import channle.signals