import logging
from ..core.config import MESSAGING_CONFIG
from .topic_manager import TopicManager
from .queue_manager import QueueManager
from .subscription_manager import SubscriptionManager

logger = logging.getLogger(__name__)

class MessagingSetup:
    def __init__(self):
        self.topic_manager = TopicManager()
        self.queue_manager = QueueManager()
        self.subscription_manager = SubscriptionManager(
            self.topic_manager, 
            self.queue_manager
        )
        self.setup_result = {}
    
    def setup_all(self):
        logger.info("🚀 Starting messaging setup...")
        
        try:
            self._create_topics()
            
            self._create_queues_and_subscriptions()
            
            logger.info("🎉 Messaging setup completed successfully!")
            return self.setup_result
            
        except Exception as e:
            logger.error(f"❌ Messaging setup failed: {e}")
            raise
    
    def _create_topics(self):
        self.setup_result["topics"] = {}
        
        for service_name, topic_config in MESSAGING_CONFIG.items():
            topic_arn = self.topic_manager.create_topic(topic_config.name)
            self.setup_result["topics"][service_name] = topic_arn
    
    def _create_queues_and_subscriptions(self):
        self.setup_result["queues"] = {}
        
        for service_name, topic_config in MESSAGING_CONFIG.items():
            self.setup_result["queues"][service_name] = []
            
            for queue_config in topic_config.queues:
                queue_info = self.subscription_manager.setup_subscription(
                    topic_config.name,
                    queue_config
                )
                self.setup_result["queues"][service_name].append(queue_info)

def setup_all():
    setup = MessagingSetup()
    return setup.setup_all()

if __name__ == "__main__":
    setup_all()