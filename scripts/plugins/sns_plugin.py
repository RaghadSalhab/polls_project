# # scripts/plugins/sns_plugin.py
from .base_plugin import AWSResourcePlugin
import botocore

class SNSPlugin(AWSResourcePlugin):
    def __init__(self):
        super().__init__('sns')
    
    def create_resource(self, client, name: str, context: dict = None):
        attributes = self.get_smart_attributes(name)
        try:
            resp = client.create_topic(Name=name, Attributes=attributes)
            return {'status': 'created', 'topic_arn': resp['TopicArn']}
        except botocore.exceptions.ClientError as e:
            raise RuntimeError(f"SNS create_topic failed for {name}: {e}")
    
    def resource_exists(self, client, name: str) -> bool:
        try:
            topics = client.list_topics().get('Topics', [])
            return any(name == t['TopicArn'].split(':')[-1] for t in topics)
        except botocore.exceptions.ClientError:
            return False
    
    def get_smart_attributes(self, name: str) -> dict:
        attrs = {}
        if any(x in name.lower() for x in ('notification', 'alert')):
            attrs['DisplayName'] = name.replace('-', ' ').title()
        return attrs
