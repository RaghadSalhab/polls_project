# my_project/app_name/management/commands/setup_localstack.py
import os
import boto3
from botocore.exceptions import ClientError
from django.core.management.base import BaseCommand
from django.conf import settings

LOCALSTACK_URL = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", None)  # optional profile

class Command(BaseCommand):
    help = "Setup LocalStack resources for local development (independent of app runtime)"

    def handle(self, *args, **kwargs):
        # 0️⃣ Production-safe: only run if LocalStack endpoint is set
        if not LOCALSTACK_URL:
            self.stdout.write("⚠️ LOCALSTACK_ENDPOINT not defined. Skipping LocalStack setup.")
            return

        self.stdout.write("⚙️ Setting up LocalStack resources...")

        # 1️⃣ Redirect *_BASE_URL in settings to LocalStack endpoints
        for key, value in list(globals().items()):
            if key.endswith('_BASE_URL') and isinstance(value, str):
                service_name = value.split('.')[0].split('//')[-1]
                globals()[key] = f"{LOCALSTACK_URL}/{service_name}"
                self.stdout.write(f"🔄 {key} → {globals()[key]}")

        # 2️⃣ Create boto3 session (support AWS profile if provided)
        session_args = {}
        if AWS_PROFILE:
            session_args['profile_name'] = AWS_PROFILE
        session = boto3.Session(**session_args)

        sqs_client = session.client(
            "sqs",
            region_name=AWS_REGION,
            aws_access_key_id="test",
            aws_secret_access_key="test",
            endpoint_url=LOCALSTACK_URL
        )

        sns_client = session.client(
            "sns",
            region_name=AWS_REGION,
            aws_access_key_id="test",
            aws_secret_access_key="test",
            endpoint_url=LOCALSTACK_URL
        )

        # 3️⃣ Provision SQS queues
        sqs_config = settings.AWS.get('SQS', {})
        for queue_group, queues in sqs_config.items():
            if isinstance(queues, dict):
                for queue_name in queues.values():
                    self.create_queue_safe(sqs_client, queue_name)
            elif isinstance(queues, str):
                self.create_queue_safe(sqs_client, queues)

        # 4️⃣ Provision SNS topics
        sns_config = settings.AWS.get('SNS', {})
        for topic_name, value in sns_config.items():
            topic_str = topic_name if isinstance(value, str) else str(value)
            self.create_topic_safe(sns_client, topic_str)

        self.stdout.write("✅ LocalStack setup complete!")

    def create_queue_safe(self, client, queue_name):
        try:
            resp = client.create_queue(QueueName=queue_name)
            url = resp['QueueUrl']
            self.stdout.write(f"📥 Created/ensured SQS queue: {queue_name} → {url}")
        except ClientError as e:
            self.stdout.write(f"❌ Failed to create SQS queue {queue_name}: {e}")

    def create_topic_safe(self, client, topic_name):
        try:
            resp = client.create_topic(Name=topic_name)
            arn = resp['TopicArn']
            settings.AWS['SNS'][topic_name] = arn
            self.stdout.write(f"📢 Created/ensured SNS topic: {topic_name} → {arn}")
        except ClientError as e:
            self.stdout.write(f"❌ Failed to create SNS topic {topic_name}: {e}")
