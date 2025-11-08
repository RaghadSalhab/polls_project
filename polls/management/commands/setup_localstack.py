import os
import boto3
from botocore.exceptions import ClientError
from django.core.management.base import BaseCommand
from django.conf import settings

# Force AWS credentials to avoid issues with multiple containers
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"

LOCALSTACK_URL = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
APP_ROLE = os.getenv("APP_ROLE", "PUBLISHER").upper()  # PUBLISHER or CONSUMER


class Command(BaseCommand):
    help = "Setup LocalStack resources (SQS/SNS) depending on the current role"

    def handle(self, *args, **kwargs):
        if not LOCALSTACK_URL:
            self.stdout.write("⚠️ LOCALSTACK_ENDPOINT not defined. Skipping LocalStack setup.")
            return

        self.stdout.write(f"\n⚙️ Setting up LocalStack resources for role: {APP_ROLE}\n")

        # Create boto3 session
        session = boto3.Session()
        sqs_client = session.client(
            "sqs",
            region_name=AWS_REGION,
            aws_access_key_id="test",
            aws_secret_access_key="test",
            endpoint_url=LOCALSTACK_URL,
        )

        sns_client = session.client(
            "sns",
            region_name=AWS_REGION,
            aws_access_key_id="test",
            aws_secret_access_key="test",
            endpoint_url=LOCALSTACK_URL,
        )


        if APP_ROLE == "CONSUMER":
            sqs_config = settings.AWS.get("SQS", {})
            for group, queues in sqs_config.items():
                if isinstance(queues, dict):
                    for queue_name in queues.values():
                        self.create_queue_safe(sqs_client, queue_name)
                elif isinstance(queues, str):
                    self.create_queue_safe(sqs_client, queues)


        elif APP_ROLE == "PUBLISHER":
            sns_config = settings.AWS.get("SNS", {})
            for topic_name, value in sns_config.items():
                real_name = value.split(":")[-1] if isinstance(value, str) and value.startswith("arn:") else str(value)
                arn = self.create_topic_safe(sns_client, real_name)
                self.stdout.write(f"📢 [Created from {APP_ROLE}] SNS topic: {topic_name} → {arn}")

        else:
            self.stdout.write(f"⚠️ Unknown APP_ROLE '{APP_ROLE}', nothing created.")

        self.stdout.write("\n✅ LocalStack setup complete!\n")


    def create_queue_safe(self, client, queue_name):
        try:
            existing = client.list_queues()
            urls = existing.get("QueueUrls", [])
            for url in urls:
                # Use last part of URL as the queue name
                if url.split("/")[-1] == queue_name:
                    self.stdout.write(f"✅ [Exists] SQS queue already exists: {queue_name} → {url}")
                    return url

            resp = client.create_queue(QueueName=queue_name)
            url = resp["QueueUrl"]
            self.stdout.write(f"📥 [Created from {APP_ROLE}] SQS queue: {queue_name} → {url}")
            return url
        except ClientError as e:
            self.stdout.write(f"❌ Failed to create SQS queue {queue_name}: {e}")
            return None

    def create_topic_safe(self, client, topic_name):
        try:
            existing = client.list_topics()
            topics = existing.get("Topics", [])
            for t in topics:
                arn = t.get("TopicArn", "")
                if arn.split(":")[-1] == topic_name:
                    self.stdout.write(f"✅ [Exists] SNS topic already exists: {topic_name} → {arn}")
                    return arn

            resp = client.create_topic(Name=topic_name)
            arn = resp["TopicArn"]
            self.stdout.write(f"📢 [Created from {APP_ROLE}] SNS topic: {topic_name} → {arn}")
            return arn
        except ClientError as e:
            self.stdout.write(f"❌ Failed to create SNS topic {topic_name}: {e}")
            return "ERROR"

