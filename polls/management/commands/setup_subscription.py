from django.core.management.base import BaseCommand
import boto3
import os
import json

class Command(BaseCommand):
    help = "Subscribe SQS queue to SNS topic in LocalStack"

    def handle(self, *args, **kwargs):
        self.stdout.write("🔄 Connecting to LocalStack...")

        # إعداد الكلاينت
        localstack_url = "http://localstack:4566"
        sns = boto3.client("sns", endpoint_url=localstack_url, region_name="us-east-1")
        sqs = boto3.client("sqs", endpoint_url=localstack_url, region_name="us-east-1")

        topic_name = "prod-team-recognition-notifications"
        queue_name = "prod-team-recognition-updates"

        # نحصل على الـ ARN تبع الـ topic
        topic_arn = sns.create_topic(Name=topic_name)["TopicArn"]

        # نحصل على ARN تبع الـ queue
        queue_url = sqs.get_queue_url(QueueName=queue_name)["QueueUrl"]
        queue_attrs = sqs.get_queue_attributes(
            QueueUrl=queue_url, AttributeNames=["QueueArn"]
        )
        queue_arn = queue_attrs["Attributes"]["QueueArn"]

        # نضيف policy تسمح لـ SNS بإرسال رسائل إلى SQS
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

        sqs.set_queue_attributes(
            QueueUrl=queue_url, Attributes={"Policy": json.dumps(policy)}
        )

        # أخيرًا نعمل subscription بينهما
        sns.subscribe(TopicArn=topic_arn, Protocol="sqs", Endpoint=queue_arn)

        self.stdout.write(
            f"✅ Subscribed {queue_name} to {topic_arn}\n🔗 SNS → SQS link established!"
        )
