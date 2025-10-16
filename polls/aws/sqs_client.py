import boto3
import os

class SQSClient:
    def __init__(self):
        self.client = boto3.client(
            "sqs",
            region_name="us-east-1",
            aws_access_key_id="test",
            aws_secret_access_key="test",
            endpoint_url=os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
        )

    def receive_messages(self, queue_url: str):
        response = self.client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=10,
            WaitTimeSeconds=5
        )
        return response.get("Messages", [])

    def delete_message(self, queue_url: str, receipt_handle: str):
        self.client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
