from polls.models.request_scope import set_current_request, get_request_id
from polls.models.database import Session

class SQLAlchemyRequestIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        set_current_request(request)
        request_id = get_request_id()
        print(f"Handling Request ID: {request_id}")  

        try:
            response = self.get_response(request)
            Session.commit()
        except Exception:
            Session.rollback()
            raise
        finally:
            Session.remove()
        return response