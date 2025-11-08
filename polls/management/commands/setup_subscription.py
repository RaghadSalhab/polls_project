#management/commands/setup_subscription.py
from django.core.management.base import BaseCommand
import boto3
import json
#python manage.py setup_subscription
TOPIC_QUEUE_CONFIG = {
    "prod-team-recognition-notifications": ["prod-team-recognition-updates", "prod-team-recognition-updates-balmm"],
    # "another-topic": ["another-queue"]
}

class Command(BaseCommand):
    help = "Subscribe SQS queues to SNS topics in LocalStack"

    def add_arguments(self, parser):
        parser.add_argument(
            "--topic", type=str, help="SNS topic name (overrides config)"
        )
        parser.add_argument(
            "--queue", type=str, help="SQS queue name (overrides config)"
        )

    def handle(self, *args, **kwargs):
        localstack_url = "http://localstack:4566"
        sns = boto3.client("sns", endpoint_url=localstack_url, region_name="us-east-1")
        sqs = boto3.client("sqs", endpoint_url=localstack_url, region_name="us-east-1")

        topics_to_process = {}

        if kwargs["topic"] and kwargs["queue"]:
            topics_to_process[kwargs["topic"]] = [kwargs["queue"]]
        else:
            topics_to_process = TOPIC_QUEUE_CONFIG

        for topic_name, queue_names in topics_to_process.items():
            self.stdout.write(f"🔄 Processing Topic: {topic_name}")
            topic_arn = sns.create_topic(Name=topic_name)["TopicArn"]

            for queue_name in queue_names:
                queue_url = sqs.get_queue_url(QueueName=queue_name)["QueueUrl"]
                queue_attrs = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=["QueueArn"])
                queue_arn = queue_attrs["Attributes"]["QueueArn"]

                existing_subs = sns.list_subscriptions_by_topic(TopicArn=topic_arn).get("Subscriptions", [])
                if any(sub.get("Endpoint") == queue_arn for sub in existing_subs):
                    self.stdout.write(f"✅ Subscription already exists: {queue_name} → {topic_name}")
                    continue

                policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": "sqs:SendMessage",
                            "Resource": queue_arn,
                            "Condition": {"ArnEquals": {"aws:SourceArn": topic_arn}},
                        }
                    ],
                }
                sqs.set_queue_attributes(QueueUrl=queue_url, Attributes={"Policy": json.dumps(policy)})

                sns.subscribe(TopicArn=topic_arn, Protocol="sqs", Endpoint=queue_arn)
                self.stdout.write(f"✅ Subscribed {queue_name} → {topic_name}")

        self.stdout.write("🔗 All subscriptions processed successfully!")
