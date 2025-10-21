import logging
from polls.messaging.handlers.base_handler import BaseEventHandler

logger = logging.getLogger(__name__)

class UserCreatedHandler(BaseEventHandler):
    def can_handle(self, event_type: str) -> bool:
        return event_type == "USER_CREATED"
    
    def handle(self, message_body: dict):
        user_id = message_body.get("user_id")
        logger.info(f"✅ User Created: {user_id}")
        return {"user_id": user_id, "status": "created"}
    

class UserUpdatedHandler(BaseEventHandler):
    def can_handle(self, event_type: str) -> bool:
        return event_type == "USER_UPDATED"
    
    def handle(self, message_body: dict):
        user_id = message_body.get("user_id")
        logger.info(f"✏️ User Updated: {user_id}")
        return {"user_id": user_id, "status": "updated"}


class UserDeletedHandler(BaseEventHandler):
    def can_handle(self, event_type: str) -> bool:
        return event_type == "USER_DELETED"
    
    def handle(self, message_body: dict):
        user_id = message_body.get("user_id")
        logger.info(f"🗑️ User Deleted: {user_id}")
        return {"user_id": user_id, "status": "deleted"}