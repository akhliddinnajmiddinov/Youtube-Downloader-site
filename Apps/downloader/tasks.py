from celery import shared_task
from .models import Query
from django.conf import settings
from django.core.files import File
import os
import yt_dlp
import logging
import uuid

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def attach_file_to_query(query, filename):
	with open(settings.MEDIA_ROOT / filename, 'rb') as local_file:
		django_file = File(local_file)
		query.downloaded_file.save(filename, django_file)


def decorator_hook(query):
    def download_progress(d):
        query.downloaded_percentage = int(float(d['_percent_str'][:-1]))
        query.save()
        if d['status'] == 'downloading':
            logging.info(f"Downloading: {d['_percent_str']} of {d.get('_total_bytes_str', 'unknown size')} at {d.get('_speed_str', 'unknown speed')}")
    
    return download_progress


def get_file_name(ext):
	return "%s.%s" % (uuid.uuid4(), ext)


@shared_task()
def download_youtube_video(query_id, output_path='media'):
    query = Query.objects.get(pk=query_id)
    url = query.url

    # Create the downloads directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    filename = get_file_name("mp4")

    ydl_opts = {
        'format': 'best',
        'outtmpl': f"{output_path}/{filename}",  # Filename format
        'quiet': True,  # Suppresses yt-dlp output; use logging instead
        'retries': 3,  # Retry failed downloads
        'progress_hooks': [decorator_hook(query)],  # Custom progress function
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            logging.info(f'Starting download: {url}')
            ydl.download([url])
            attach_file_to_query(query, filename)
            logging.info('Download completed successfully!')
    except Exception as e:
        logging.error(f'An error occurred: {e}')
