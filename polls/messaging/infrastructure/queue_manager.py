import json
import logging
from typing import Dict, Optional, Tuple 
from ..core.clients import sqs

logger = logging.getLogger(__name__)

class QueueManager:
    def __init__(self):
        self.existing_queues = {}
        self._load_existing_queues()
    
    def _load_existing_queues(self):
        try:
            response = sqs.list_queues()
            for queue_url in response.get("QueueUrls", []):
                queue_name = queue_url.split("/")[-1]
                self.existing_queues[queue_name] = queue_url
        except Exception as e:
            logger.error(f"Failed to load existing queues: {e}")
    
    def create_queue(self, name: str, dlq_name: Optional[str] = None) -> Dict:

        queue_url, queue_arn = self._get_or_create_queue(name)
        
        dlq_arn = None
        if dlq_name:
            dlq_url, dlq_arn = self._get_or_create_queue(dlq_name)
            self._attach_dlq_policy(queue_url, queue_arn, dlq_arn)
        
        return {
            "url": queue_url,
            "arn": queue_arn,
            "dlq_arn": dlq_arn
        }
    
    def _get_or_create_queue(self, name: str) -> Tuple[str, str]:
        if name in self.existing_queues:
            queue_url = self.existing_queues[name]
            queue_arn = self._get_queue_arn(queue_url)
            print(f"✅ Queue already exists: {queue_url}")
            return queue_url, queue_arn
        
        try:
            response = sqs.create_queue(QueueName=name)
            queue_url = response["QueueUrl"]
            queue_arn = self._get_queue_arn(queue_url)
            self.existing_queues[name] = queue_url
            print(f"✅ Queue created: {queue_url}")
            return queue_url, queue_arn
        except Exception as e:
            print(f"❌ Failed to create queue {name}: {e}")
            raise
    
    def _get_queue_arn(self, queue_url: str) -> str:
        attrs = sqs.get_queue_attributes(
            QueueUrl=queue_url, 
            AttributeNames=["QueueArn"]
        )
        return attrs["Attributes"]["QueueArn"]
    
    def _attach_dlq_policy(self, queue_url: str, queue_arn: str, dlq_arn: str):
        redrive_policy = {
            "deadLetterTargetArn": dlq_arn,
            "maxReceiveCount": "3"
        }
        
        sqs.set_queue_attributes(
            QueueUrl=queue_url,
            Attributes={"RedrivePolicy": json.dumps(redrive_policy)}
        )
        logger.info(f"🔄 DLQ policy attached: {queue_url} → {dlq_arn}")