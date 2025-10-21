import logging
from .base_handler import BaseEventHandler
from polls.services.choice_service import ChoiceService

logger = logging.getLogger(__name__) 

class QuestionCreatedHandler(BaseEventHandler):
    def can_handle(self, event_type: str) -> bool:
        return event_type in ["QUESTION_CREATED", "QUESTION_UPDATED"]
    
    def handle(self, message_body: dict):
        def operation():
            user_id = message_body.get("user_id")
            question_id = message_body.get("question_id")
            choices = message_body.get("choices", [])
            
            existing_choices = ChoiceService.list_choices_for_question(question_id)
            existing_texts = {c['choice_text']: c['id'] for c in existing_choices}
            
            for choice_data in choices:
                if isinstance(choice_data, str):
                    choice_data = {"choice_text": choice_data, "id": None}

                choice_text = choice_data.get("choice_text")
                choice_id = choice_data.get("id") or existing_texts.get(choice_text)
                
                if choice_id:
                    ChoiceService.update_choice(user_id, choice_id, choice_text)
                    logger.info(f"✏️ Choice Updated: {choice_id}")  
                else:
                    choice = ChoiceService.create_choice(user_id, question_id, choice_text)
                    logger.info(f"✅ Choice Created: {choice['id']}")

            return True
        
        return self._execute_safely(operation)
    
class ChoiceUpdatedHandler(BaseEventHandler):  
    def can_handle(self, event_type: str) -> bool:
        return event_type == "CHOICE_UPDATED"
    
    def handle(self, message_body: dict):
        def operation():
            choice_id = message_body.get("choice_id")
            user_id = message_body.get("user_id")
            choice_text = message_body.get("choice_text")
            
            choice = ChoiceService.update_choice(user_id, choice_id, choice_text)
            logger.info(f"✏️ Choice Updated via event: {choice_id}")
            return {"choice_id": choice_id, "status": "updated"}
        
        return self._execute_safely(operation)  

class ChoiceVotedHandler(BaseEventHandler):
    def can_handle(self, event_type: str) -> bool:
        return event_type == "CHOICE_VOTED"
    
    def handle(self, message_body: dict):
        logger.info(f"🗳️ Vote processed for choice: {message_body.get('choice_id')}")
        return {"choice_id": message_body.get('choice_id'), "status": "voted"}