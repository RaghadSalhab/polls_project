from polls.models.database import Session

def db_session_middleware(get_response):
    def middleware(request):
        try:
            response = get_response(request)
            Session.commit()  
        except Exception:
            Session.rollback()
            raise
        finally:
            Session.remove()  
        return response
    return middleware
