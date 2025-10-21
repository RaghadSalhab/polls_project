import json
import logging
from abc import ABC, abstractmethod
from polls.messaging.core.clients import sqs
from polls.models.database import Session

logger = logging.getLogger(__name__)

class BaseConsumer(ABC):
    def __init__(self, queue_url):
        self.queue_url = queue_url
    
    def consume(self, wait_time=3, max_messages=5):
        print(f"🚀 Starting consumer for {self.queue_url}")
        
        while True:
            try:
                response = sqs.receive_message(
                    QueueUrl=self.queue_url,
                    MaxNumberOfMessages=max_messages,
                    WaitTimeSeconds=wait_time,
                    MessageAttributeNames=["All"]
                )
                
                for msg in response.get("Messages", []):
                    self._process_single_message(msg)
                        
            except Exception as e:
                print(f"❌ Consumer error: {e}")
    
    def _process_single_message(self, message):
        try:
            message_body = self._extract_message_body(message)
            event_type = message_body.get("event")
            
            handler = self.get_handler(event_type)
            if not handler:
                print(f"⚠️ No handler for event: {event_type}")
                return
            
            handler.handle(message_body)
            
            sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=message["ReceiptHandle"]
            )
            
        except Exception as e:
            logger.error(f"❌ Failed to process message: {e}")
    
    def _extract_message_body(self, message):
        body = message["Body"]
        
        if isinstance(body, str):
            body = json.loads(body)
        
        if "Message" in body:
            msg = body["Message"]
            if isinstance(msg, str):
                msg = json.loads(msg)
            return msg
        
        return body

    @abstractmethod
    def get_handler(self, event_type):
        pass