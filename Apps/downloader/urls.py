from django.urls import path
from .views import DownloadPageView, GetFileView
from .api import api_get_downloading_progress

app_name = 'downloader'
urlpatterns = [
	path('', DownloadPageView, name='downloader'),
	path('api_get_downloading_progress', api_get_downloading_progress, name='api_get_downloading_progress'),
	path('get_file', GetFileView, name='get_file')
]