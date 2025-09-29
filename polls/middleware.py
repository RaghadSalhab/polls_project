from polls.models.database import SessionLocal

def db_session_middleware(get_response):
    def middleware(request):
        request.db = SessionLocal()
        try:
            response = get_response(request)
            request.db.commit()
        except Exception:
            request.db.rollback()
            raise
        finally:
            request.db.close()
        return response
    return middleware
