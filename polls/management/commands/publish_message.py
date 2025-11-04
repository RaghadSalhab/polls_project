#management/commands/publish_message.py
import os
import boto3
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Send a test message to SNS topic"

    def handle(self, *args, **kwargs):
        sns = boto3.client(
            "sns",
            aws_access_key_id="test",
            aws_secret_access_key="test",
            region_name="us-east-1",
            endpoint_url=os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
        )

        topic_arn = "arn:aws:sns:us-east-1:000000000000:prod-team-recognition-notifications"

        sns.publish(
            TopicArn=topic_arn,
            Message="🎉 Hello from Publisher!"
        )

        self.stdout.write("✅ Message sent to SNS!")
