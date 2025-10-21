import json
import logging
from .clients import sns

logger = logging.getLogger(__name__)

class EventPublisher:
    
    TOPICS = {
        "question": "arn:aws:sns:us-east-1:000000000000:question-topic",
        "choice": "arn:aws:sns:us-east-1:000000000000:choice-topic",
        "user": "arn:aws:sns:us-east-1:000000000000:user-topic",
        "stats": "arn:aws:sns:us-east-1:000000000000:stats-topic"
    }
    
    @classmethod
    def publish_question_event(cls, event_type: str, data: dict):
        return cls._publish_event("question", event_type, data)
    
    @classmethod
    def publish_choice_event(cls, event_type: str, data: dict):
        return cls._publish_event("choice", event_type, data)
    
    @classmethod
    def publish_user_event(cls, event_type: str, data: dict):
        return cls._publish_event("user", event_type, data)
    
    @classmethod
    def publish_stats_event(cls, event_type: str, data: dict):
        return cls._publish_event("stats", event_type, data)
    
    @classmethod
    def _publish_event(cls, service: str, event_type: str, data: dict):
        try:
            message = {
                "event": event_type,
                **data
            }
            
            response = sns.publish(
                TopicArn=cls.TOPICS[service],
                Message=json.dumps(message),
                MessageAttributes={
                    "event_type": {"DataType": "String", "StringValue": event_type}
                }
            )
            
            logger.info(f"📤 Event published: {event_type} to {service} topic")
            return response
            
        except Exception as e:
            logger.error(f"❌ Failed to publish event {event_type}: {e}")
            return None