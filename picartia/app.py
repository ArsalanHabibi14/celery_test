"""
    Celery Configuration
"""

from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "picartia.settings")

app = Celery("picartia")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
