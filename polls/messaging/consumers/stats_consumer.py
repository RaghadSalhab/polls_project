import os
import logging
from polls.messaging.consumers.base_consumer import BaseConsumer
from polls.messaging.handlers.handler_registry import stats_registry

logger = logging.getLogger(__name__)
# STATS_QUEUE_URL = os.getenv("STATS_QUEUE_URL")
from django.conf import settings

STATS_QUEUE_URL = settings.AWS["SQS"]["STATS"]["STATS_QUEUE"]

class StatsConsumer(BaseConsumer):
    
    def __init__(self):
        super().__init__(STATS_QUEUE_URL)
    
    def get_handler(self, event_type):
        return stats_registry.get_handler(event_type)

def consume_stats_queue():
    consumer = StatsConsumer()
    consumer.consume()