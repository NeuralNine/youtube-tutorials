# NOTE: This file is new

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "celery_example.settings")

celery_app = Celery('movie_project')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

