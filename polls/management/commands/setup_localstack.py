
# import os
# import boto3
# from botocore.exceptions import ClientError
# from django.core.management.base import BaseCommand
# from django.conf import settings

# LOCALSTACK_URL = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
# AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
# AWS_PROFILE = os.getenv("AWS_PROFILE", None)
# ROLE = os.getenv("APP_ROLE", "PUBLISHER").upper()  # Publisher أو Consumer


# class Command(BaseCommand):
#     help = "Setup LocalStack resources for local development (independent of app runtime)"

#     def handle(self, *args, **kwargs):
#         if not LOCALSTACK_URL:
#             self.stdout.write("⚠️ LOCALSTACK_ENDPOINT not defined. Skipping LocalStack setup.")
#             return

#         self.stdout.write(f"⚙️ Setting up LocalStack resources for role: {ROLE}\n")

#         session_args = {}
#         if AWS_PROFILE:
#             session_args['profile_name'] = AWS_PROFILE
#         session = boto3.Session(**session_args)

#         sqs_client = session.client(
#             "sqs",
#             region_name=AWS_REGION,
#             aws_access_key_id="test",
#             aws_secret_access_key="test",
#             endpoint_url=LOCALSTACK_URL
#         )

#         sns_client = session.client(
#             "sns",
#             region_name=AWS_REGION,
#             aws_access_key_id="test",
#             aws_secret_access_key="test",
#             endpoint_url=LOCALSTACK_URL
#         )

#         if ROLE == "CONSUMER":
#             # Consumer → فقط SQS
#             sqs_config = settings.AWS.get('SQS', {})
#             for queue_group, queues in sqs_config.items():
#                 if isinstance(queues, dict):
#                     for queue_name in queues.values():
#                         self.create_queue_safe(sqs_client, queue_name)
#                 elif isinstance(queues, str):
#                     self.create_queue_safe(sqs_client, queues)

#         elif ROLE == "PUBLISHER":
#             # Publisher → فقط SNS
#             sns_config = settings.AWS.get('SNS', {})
#             for topic_name, value in sns_config.items():
#                 if isinstance(value, str) and value.startswith("arn:"):
#                     real_name = value.split(":")[-1]
#                 else:
#                     real_name = value if isinstance(value, str) else str(value)
#                 arn = self.create_topic_safe(sns_client, real_name)
#                 self.stdout.write(f"📢 {topic_name}: {arn}")

#         self.stdout.write("\n✅ LocalStack setup complete!")

#     def create_queue_safe(self, client, queue_name):
#         try:
#             resp = client.create_queue(QueueName=queue_name)
#             url = resp['QueueUrl']
#             self.stdout.write(f"📥 [Created from {ROLE}] SQS queue: {queue_name} → {url}")
#         except ClientError as e:
#             self.stdout.write(f"❌ [Failed {ROLE}] SQS queue {queue_name}: {e}")

#     def create_topic_safe(self, client, topic_name):
#         try:
#             resp = client.create_topic(Name=topic_name)
#             arn = resp['TopicArn']
#             self.stdout.write(f"📢 [Created from {ROLE}] SNS topic: {topic_name} → {arn}")
#             return arn
#         except ClientError as e:
#             self.stdout.write(f"❌ [Failed {ROLE}] SNS topic {topic_name}: {e}")
#             return "ERROR"
import os
import boto3
from botocore.exceptions import ClientError
from django.core.management.base import BaseCommand
from django.conf import settings

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

        # =======================================================
        # CONSUMER → Creates SQS queues
        # =======================================================
        if APP_ROLE == "CONSUMER":
            sqs_config = settings.AWS.get("SQS", {})
            for group, queues in sqs_config.items():
                if isinstance(queues, dict):
                    for queue_name in queues.values():
                        self.create_queue_safe(sqs_client, queue_name)
                elif isinstance(queues, str):
                    self.create_queue_safe(sqs_client, queues)

        # =======================================================
        # PUBLISHER → Creates SNS topics
        # =======================================================
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
            resp = client.create_queue(QueueName=queue_name)
            url = resp["QueueUrl"]
            self.stdout.write(f"📥 [Created from {APP_ROLE}] SQS queue: {queue_name} → {url}")
        except ClientError as e:
            self.stdout.write(f"❌ Failed to create SQS queue {queue_name}: {e}")

    def create_topic_safe(self, client, topic_name):
        try:
            resp = client.create_topic(Name=topic_name)
            return resp["TopicArn"]
        except ClientError as e:
            self.stdout.write(f"❌ Failed to create SNS topic {topic_name}: {e}")
            return "ERROR"
        
    def subscribe_queue_to_topic(self, sns_client, sqs_client, topic_arn, queue_name):
        queue_url = sqs_client.get_queue_url(QueueName=queue_name)['QueueUrl']
        queue_attrs = sqs_client.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['QueueArn']
        )
        queue_arn = queue_attrs['Attributes']['QueueArn']

        # نضيف صلاحيات للـ SNS إنه يقدر يرسل للـ SQS
        policy = f"""{{
            "Version": "2012-10-17",
            "Statement": [
                {{
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "sqs:SendMessage",
                    "Resource": "{queue_arn}",
                    "Condition": {{
                        "ArnEquals": {{
                            "aws:SourceArn": "{topic_arn}"
                        }}
                    }}
                }}
            ]
        }}"""

        sqs_client.set_queue_attributes(
            QueueUrl=queue_url,
            Attributes={"Policy": policy}
        )

        # إنشاء الاشتراك بين SNS و SQS
        sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='sqs',
            Endpoint=queue_arn
        )

        self.stdout.write(f"🔗 Subscribed {queue_name} to {topic_arn}")
