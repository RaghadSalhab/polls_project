import os
import logging
from .base_consumer import BaseConsumer
from polls.messaging.handlers.handler_registry import user_registry

logger = logging.getLogger(__name__)
# USER_QUEUE_URL = os.getenv("USER_QUEUE_URL")
from django.conf import settings
USER_QUEUE_URL = settings.AWS["SQS"]["USER"]["USER_QUEUE"]

class UserConsumer(BaseConsumer):
    def __init__(self):
        super().__init__(USER_QUEUE_URL)
    
    def get_handler(self, event_type):
        return user_registry.get_handler(event_type)

def consume_user_queue():
    consumer = UserConsumer()
    consumer.consume()