import os
from .base_consumer import BaseConsumer
from polls.messaging.handlers.handler_registry import choice_registry

CHOICE_QUEUE_URL = os.getenv("CHOICE_QUEUE_URL")

class ChoiceConsumer(BaseConsumer):
    def __init__(self):
        super().__init__(CHOICE_QUEUE_URL)
    
    def get_handler(self, event_type):
        return choice_registry.get_handler(event_type)

def consume_choice_queue():
    consumer = ChoiceConsumer()
    consumer.consume()