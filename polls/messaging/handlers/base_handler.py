
from abc import ABC, abstractmethod
import logging
import uuid
from polls.models.request_scope import set_current_request
from polls.models.database import Session  

logger = logging.getLogger(__name__)

class FakeRequest:
    def __init__(self):
        self.id = str(uuid.uuid4())

class BaseEventHandler(ABC):
    @abstractmethod
    def can_handle(self, event_type: str) -> bool:
        pass
    
    @abstractmethod
    def handle(self, message_body: dict):
        pass
    
    def _execute_safely(self, operation):
        request = FakeRequest()
        set_current_request(request)
        
        try:
            result = operation()
            Session.commit()
            logger.info("✅ Operation completed successfully")
            return result
        except Exception as e:
            Session.rollback()
            logger.error(f"❌ Operation failed: {e}")
            raise
        finally:
            Session.remove()