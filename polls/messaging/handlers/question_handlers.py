import logging
from polls.messaging.handlers.base_handler import BaseEventHandler
from polls.repositories.question_repository import QuestionRepository
from polls.models.database import Session

logger = logging.getLogger(__name__)

class QuestionCreatedHandler(BaseEventHandler):
    def can_handle(self, event_type: str) -> bool:
        return event_type == "QUESTION_CREATED"
    
    def handle(self, message_body: dict):
        def operation():
            question_id = message_body.get("question_id")
            user_id = message_body.get("user_id")
            question_text = message_body.get("question_text")
            
            question = QuestionRepository.get(question_id)
            if not question:
                question = QuestionRepository.add(
                    QuestionRepository.model(
                        id=question_id,
                        created_by_id=user_id,
                        question_text=question_text
                    )
                )
                logger.info(f"✅ Question Created: {question.id} by User {user_id}")
            else:
                logger.info(f"✅ Question Already Exists: {question.id}")
            
            return {"question_id": question.id, "status": "created"}
        
        return self._execute_safely(operation)  
    


class QuestionUpdatedHandler(BaseEventHandler):
    def can_handle(self, event_type: str) -> bool:
        return event_type == "QUESTION_UPDATED"
    
    def handle(self, message_body: dict):
        def operation():
            question_id = message_body.get("question_id")
            user_id = message_body.get("user_id")
            question_text = message_body.get("question_text")
            
            question = QuestionRepository.get(question_id)
            if question:
                question.question_text = question_text
                Session.commit()
                logger.info(f"✏️ Question Updated: {question.id} by User {user_id}")
                return {"question_id": question.id, "status": "updated"}
            else:
                logger.warning(f"⚠️ Question {question_id} not found for update")
                return {"question_id": question_id, "status": "not_found"}
        
        return self._execute_safely(operation)  



class QuestionDeletedHandler(BaseEventHandler):
    def can_handle(self, event_type: str) -> bool:
        return event_type == "QUESTION_DELETED"
    
    def handle(self, message_body: dict):
        def operation():
            question_id = message_body.get("question_id")
            
            deleted = QuestionRepository.delete_by_id(question_id, commit=True)
            if deleted:
                logger.info(f"🗑️ Question Deleted: {question_id}")
                return {"question_id": question_id, "status": "deleted"}
            else:
                logger.warning(f"⚠️ Question {question_id} not found for deletion")
                return {"question_id": question_id, "status": "not_found"}
        
        return self._execute_safely(operation)  
