import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'youtube_downloader_site.settings')
app = Celery('youtube_downloader_site')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
