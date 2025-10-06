import threading
import uuid

_thread_local = threading.local()

def set_current_request(request):
    _thread_local.request = request
    _thread_local.request_id = str(uuid.uuid4())

def get_current_request():
    return getattr(_thread_local, "request_id", None)

def get_request_id():
    return getattr(_thread_local, "request_id", None)