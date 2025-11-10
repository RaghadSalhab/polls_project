from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
import json

def proxy_view(request, path):
    if request.body:
        try:
            request_data = json.loads(request.body)
        except:
            request_data = {"raw_body": request.body.decode()}
    else:
        request_data = dict(request.GET)

    ai_response = {
        "message": f"AI-generated response for path: /{path}",
        "request_received": request_data
    }

    return JsonResponse(ai_response)
