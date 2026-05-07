default_app_config = 'config.apps.ConfigConfig'

from .celery import app as celery_app

__all__ = ('celery_app',)