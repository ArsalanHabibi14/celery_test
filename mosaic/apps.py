from django.apps import AppConfig


class MosaicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mosaic'

    def ready(self):
        from . import signals