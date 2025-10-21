import logging
from polls.messaging.handlers.base_handler import BaseEventHandler
from polls.services.stats_service import StatsService

logger = logging.getLogger(__name__)  

class ChoiceVotedHandler(BaseEventHandler):
    
    def can_handle(self, event_type: str) -> bool:
        return event_type == "CHOICE_VOTED"
    
    def handle(self, message_body: dict):
        def operation():
            question_id = message_body.get("question_id")
            choice_id = message_body.get("choice_id")
            
            logger.info(f"📩 Processing CHOICE_VOTED for Question {question_id}, Choice {choice_id}")  
            
            votes = StatsService.get_question_votes(question_id)
            top_question = StatsService.get_top_question()
            top_choice = StatsService.get_top_choice()
            
            StatsService.list_questions_with_votes()
            
            logger.info(f"📊 Stats updated for Question {question_id}: total votes = {votes}")  
            logger.info(f"🏆 Top Question: {top_question and top_question.get('question_text')}")  
            logger.info(f"🥇 Top Choice: {top_choice and top_choice.get('choice_text')}")  
            
            return {
                "question_id": question_id,
                "total_votes": votes,
                "top_question": top_question,
                "top_choice": top_choice
            }
        
        return self._execute_safely(operation) 

class QuestionCreatedHandler(BaseEventHandler):    
    def can_handle(self, event_type: str) -> bool:
        return event_type == "QUESTION_CREATED"
    
    def handle(self, message_body: dict):
        def operation():
            question_id = message_body.get("question_id")
            logger.info(f"📊 Initializing stats for new question: {question_id}")  
            
            return {"question_id": question_id, "status": "stats_initialized"}
        
        return self._execute_safely(operation)  

class UserVotedHandler(BaseEventHandler):
    
    def can_handle(self, event_type: str) -> bool:
        return event_type == "USER_VOTED"
    
    def handle(self, message_body: dict):
        def operation():
            user_id = message_body.get("user_id")
            question_id = message_body.get("question_id")
            
            logger.info(f"👤 User {user_id} voted on question {question_id}") 
            
            return {"user_id": user_id, "question_id": question_id}
        
        return self._execute_safely(operation)  
