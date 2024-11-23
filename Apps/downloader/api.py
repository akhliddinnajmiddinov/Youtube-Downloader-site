from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Query
from .security import decode
import json


def api_get_downloading_progress(request):
	if request.method == "POST":
		data = json.loads(request.body)
		query_id = decode(data['query_token'])["query_id"]
		
		query = get_object_or_404(Query, pk=query_id)
		
		context = {
			"downloaded_percentage": query.downloaded_percentage,
			"file_path": "/get_file?filename=" + query.downloaded_file.url.rsplit('/', 1)[1] if query.downloaded_percentage == 100 else ""
		}

		return JsonResponse(context)
