import os
import logging
from .base_consumer import BaseConsumer
from polls.messaging.handlers.handler_registry import question_registry

logger = logging.getLogger(__name__)
# QUESTION_QUEUE_URL = os.getenv("QUESTION_QUEUE_URL")
from django.conf import settings

QUESTION_QUEUE_URL = settings.AWS["SQS"]["QUESTION"]["QUESTION_QUEUE"]

class QuestionConsumer(BaseConsumer):
    def __init__(self):
        super().__init__(QUESTION_QUEUE_URL)
    
    def get_handler(self, event_type):
        return question_registry.get_handler(event_type)

def consume_question_queue():
    consumer = QuestionConsumer()
    consumer.consume()