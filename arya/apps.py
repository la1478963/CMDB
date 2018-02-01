from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules

class AryaConfig(AppConfig):
    name = 'arya'
    def ready(self):
        autodiscover_modules('arya')
