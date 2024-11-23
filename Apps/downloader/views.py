from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import Query
from .tasks import download_youtube_video
from .security import encode
import json
import mimetypes


def send_file(path, filename = None):

    if filename is None: filename = os.path.basename(path)

    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=%s' %filename
    response.write(open(path, "rb").read())
    return response


def DownloadPageView(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		query = Query(url=data['url'], quality='best')
		query.save()

		download_youtube_video.delay(query_id=query.pk)
		return JsonResponse({"query_token": encode({ "query_id": query.pk })})

	return render(request, "downloader.html")


def GetFileView(request):
	filename = request.GET.get('filename')
	return send_file(path=f"media/{filename}", filename=filename)