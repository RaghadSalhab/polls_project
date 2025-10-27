# scripts/plugins/sqs_plugin.py
from .base_plugin import AWSResourcePlugin
import botocore

class SQSPlugin(AWSResourcePlugin):
    def __init__(self):
        super().__init__('sqs')
    
    def create_resource(self, client, name: str, context: dict = None):
        attributes = self.get_smart_attributes(name)
        try:
            resp = client.create_queue(QueueName=name, Attributes=attributes)
            return {'status': 'created', 'queue_url': resp['QueueUrl']}
        except botocore.exceptions.ClientError as e:
            raise RuntimeError(f"SQS create_queue failed for {name}: {e}")
    
    def resource_exists(self, client, name: str) -> bool:
        try:
            urls = client.list_queues().get('QueueUrls', [])
            return any(name == url.split('/')[-1] for url in urls)
        except botocore.exceptions.ClientError:
            return False
    
    def get_smart_attributes(self, name: str) -> dict:
        attrs = {
            'DelaySeconds': '0',
            'VisibilityTimeout': '30',
            'ReceiveMessageWaitTimeSeconds': '0'
        }
        n = name.lower()
        if any(x in n for x in ('deadletter', 'dlq')):
            attrs['MessageRetentionPeriod'] = '1209600'
        if any(x in n for x in ('notification', 'alert')):
            attrs['VisibilityTimeout'] = '60'
        if any(x in n for x in ('process', 'batch')):
            attrs['VisibilityTimeout'] = '300'
        return attrs
