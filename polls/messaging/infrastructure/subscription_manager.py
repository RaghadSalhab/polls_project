import json
import logging
from typing import Dict, Optional  
from ..core.clients import sns, sqs

logger = logging.getLogger(__name__)

class SubscriptionManager:
    def __init__(self, topic_manager, queue_manager):
        self.topic_manager = topic_manager
        self.queue_manager = queue_manager
    
    def setup_subscription(self, topic_name: str, queue_config):
        topic_arn = self.topic_manager.existing_topics[topic_name]
        queue_info = self.queue_manager.create_queue(
            queue_config.name, 
            queue_config.dlq_name
        )
        
        self._attach_sns_policy(queue_info["arn"], topic_arn, queue_info["url"])
        
        self._create_subscription(
            topic_arn, 
            queue_info["arn"], 
            queue_config.filter_policy
        )
        
        return queue_info
    
    def _attach_sns_policy(self, queue_arn: str, topic_arn: str, queue_url: str):
        policy = {
            "Version": "2012-10-17",
            "Statement": [{
                "Effect": "Allow",
                "Principal": "*",
                "Action": "sqs:SendMessage",
                "Resource": queue_arn,
                "Condition": {"ArnEquals": {"aws:SourceArn": topic_arn}}
            }]
        }
        
        sqs.set_queue_attributes(
            QueueUrl=queue_url,
            Attributes={"Policy": json.dumps(policy)}
        )
        logger.info(f"🔑 SNS policy attached to {queue_url}")
    
    def _create_subscription(self, topic_arn: str, queue_arn: str, filter_policy: Optional[Dict] = None):
        existing_subs = sns.list_subscriptions_by_topic(TopicArn=topic_arn)["Subscriptions"]
        for sub in existing_subs:
            if sub["Endpoint"] == queue_arn:
                logger.info(f"🔗 Subscription already exists: {topic_arn} → {queue_arn}")
                return
        
        params = {
            "TopicArn": topic_arn,
            "Protocol": "sqs", 
            "Endpoint": queue_arn
        }
        
        if filter_policy:
            params["Attributes"] = {"FilterPolicy": json.dumps(filter_policy)}
        
        sns.subscribe(**params)
        logger.info(f"🔗 Subscription created: {topic_arn} → {queue_arn}")