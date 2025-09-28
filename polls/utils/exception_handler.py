from rest_framework.views import exception_handler
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from rest_framework.response import Response

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        return response

    if isinstance(exc, ObjectDoesNotExist):
        return Response({"detail": str(exc)}, status=404)
    elif isinstance(exc, PermissionDenied):
        return Response({"detail": str(exc)}, status=403)

    return Response({"detail": "Unexpected error"}, status=400)
