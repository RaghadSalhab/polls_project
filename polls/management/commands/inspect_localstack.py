# import os
# import boto3
# from django.core.management.base import BaseCommand
# # python manage.py inspect_localstack
# os.environ["AWS_ACCESS_KEY_ID"] = "test"
# os.environ["AWS_SECRET_ACCESS_KEY"] = "test"

# LOCALSTACK_URL = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
# AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")


# class Command(BaseCommand):
#     help = "Inspect LocalStack SNS/SQS setup to discover microservice communication."

#     def handle(self, *args, **kwargs):
#         session = boto3.Session()
#         sqs = session.client("sqs", region_name=AWS_REGION, endpoint_url=LOCALSTACK_URL)
#         sns = session.client("sns", region_name=AWS_REGION, endpoint_url=LOCALSTACK_URL)

#         self.stdout.write("\n🔍 Inspecting LocalStack resources...\n")

#         # --- Discover Queues ---
#         queues = sqs.list_queues().get("QueueUrls", [])
#         self.stdout.write("📬 Queues found:")
#         if queues:
#             for q in queues:
#                 self.stdout.write(f"  - {q.split('/')[-1]}")
#         else:
#             self.stdout.write("⚠️ No SQS queues found!")

#         # --- Discover Topics ---
#         topics = sns.list_topics().get("Topics", [])
#         self.stdout.write("\n📢 Topics found:")
#         if topics:
#             for t in topics:
#                 self.stdout.write(f"  - {t['TopicArn'].split(':')[-1]}")
#         else:
#             self.stdout.write("⚠️ No SNS topics found!")

#         # --- Discover Subscriptions & Extract Microservice Names ---
#         ms_names = []
#         self.stdout.write("\n🔗 Subscriptions:")
#         for t in topics:
#             topic_arn = t["TopicArn"]
#             topic_name = topic_arn.split(":")[-1]
#             subs = sns.list_subscriptions_by_topic(TopicArn=topic_arn).get("Subscriptions", [])
#             if subs:
#                 for s in subs:
#                     endpoint = s.get("Endpoint", "unknown")
#                     self.stdout.write(f"  🔸 {topic_name} → {endpoint}")

#                     # Extract microservice name after 'prod'
#                     parts = endpoint.lower().split("prod")
#                     if len(parts) > 1 and parts[1]:
#                         ms_name = parts[1].strip("_-")
#                         if ms_name and ms_name not in ms_names:
#                             ms_names.append(ms_name)
#             else:
#                 self.stdout.write(f"  ⚪ {topic_name} has no subscribers.")

#         self.stdout.write(f"\n🗂 Discovered microservice names: {ms_names}")
#         self.stdout.write("\n✅ Inspection complete!\n")
#python manage.py inspect_localstack
import os
import boto3
from django.core.management.base import BaseCommand

os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"

LOCALSTACK_URL = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")


class Command(BaseCommand):
    help = "Inspect LocalStack SNS/SQS setup to discover microservice communication."

    def handle(self, *args, **kwargs):
        ms_names = self.get_microservices()
        # 👇 اطبع فقط الأسماء مفصولة بفواصل، بدون أي رموز أو نصوص إضافية
        print(",".join(ms_names))

    def get_microservices(self):
        """ترجع قائمة microservices من LocalStack"""
        session = boto3.Session()
        sqs = session.client("sqs", region_name=AWS_REGION, endpoint_url=LOCALSTACK_URL)
        sns = session.client("sns", region_name=AWS_REGION, endpoint_url=LOCALSTACK_URL)

        try:
            queues = sqs.list_queues().get("QueueUrls", [])
        except Exception:
            queues = []

        try:
            topics = sns.list_topics().get("Topics", [])
        except Exception:
            topics = []

        ms_names = []
        for t in topics:
            topic_arn = t["TopicArn"]
            subs = sns.list_subscriptions_by_topic(TopicArn=topic_arn).get("Subscriptions", [])
            for s in subs:
                endpoint = s.get("Endpoint", "")
                if not endpoint:
                    continue
                parts = endpoint.lower().split("prod")
                if len(parts) > 1 and parts[1]:
                    ms_name = parts[1].strip("_-/")
                    if ms_name and ms_name not in ms_names:
                        ms_names.append(ms_name)

        return ms_names
