#management/commands/consume_messages.py
import os
import boto3
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Consume messages from SQS"

    def handle(self, *args, **kwargs):
        sqs = boto3.client(
            "sqs",
            aws_access_key_id="test",
            aws_secret_access_key="test",
            region_name="us-east-1",
            endpoint_url=os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
        )

        queue_url = sqs.get_queue_url(QueueName="prod-team-recognition-updates")['QueueUrl']

        self.stdout.write("👂 Listening for messages...")

        while True:
            messages = sqs.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=1,
                WaitTimeSeconds=5
            ).get('Messages', [])

            for msg in messages:
                body = msg['Body']
                self.stdout.write(f"📩 Received: {body}")

                sqs.delete_message(
                    QueueUrl=queue_url,
                    ReceiptHandle=msg['ReceiptHandle']
                )
