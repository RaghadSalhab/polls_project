import logging
from ..core.clients import sns

logger = logging.getLogger(__name__)

class TopicManager:
    def __init__(self):
        self.existing_topics = {}
        self._load_existing_topics()
    
    def _load_existing_topics(self):
        try:
            response = sns.list_topics()
            for topic in response.get("Topics", []):
                topic_name = topic["TopicArn"].split(":")[-1]
                self.existing_topics[topic_name] = topic["TopicArn"]
        except Exception as e:
            logger.error(f"Failed to load existing topics: {e}")
    
    def create_topic(self, name: str) -> str:
        if name in self.existing_topics:
            logger.info(f"✅ Topic already exists: {self.existing_topics[name]}")
            return self.existing_topics[name]
        
        try:
            response = sns.create_topic(Name=name)
            topic_arn = response["TopicArn"]
            self.existing_topics[name] = topic_arn
            logger.info(f"✅ Topic created: {topic_arn}")
            return topic_arn
        except Exception as e:
            logger.error(f"❌ Failed to create topic {name}: {e}")
            raise