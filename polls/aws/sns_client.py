import json
import boto3
import os

class SNSClient:
    def __init__(self):
        self.client = boto3.client(
            "sns",
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test",
            endpoint_url=os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
        )

    def publish(self, topic_arn, message: dict):
        self.client.publish(
            TopicArn=topic_arn,
            Message=json.dumps(message)
        )
