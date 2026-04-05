from django.apps import AppConfig


import os

class ConfigConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'config'

    def ready(self):
        
        if os.getenv('RENDER') == 'true':
            return

        from scheduler import start
        start()