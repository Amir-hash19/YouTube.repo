from celery import Celery
import os



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'YouTube.settings')

app = Celery('YouTube')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
