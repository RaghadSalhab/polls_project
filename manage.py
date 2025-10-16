
"""Django's command-line utility for administrative tasks."""
import os
import sys
import boto3

endpoint = "http://localhost:4566"
region = "us-east-1"

sns = boto3.client("sns", region_name=region, endpoint_url=endpoint)
sqs = boto3.client("sqs", region_name=region, endpoint_url=endpoint)

# Create SNS topic
topic = sns.create_topic(Name="QuestionEvents")
topic_arn = topic["TopicArn"]

# Create SQS queue
queue = sqs.create_queue(QueueName="QuestionQueue")
queue_url = queue["QueueUrl"]

# Subscribe SQS to SNS
queue_arn = sqs.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=["QueueArn"]
)["Attributes"]["QueueArn"]

sns.subscribe(TopicArn=topic_arn, Protocol="sqs", Endpoint=queue_arn)

print("✅ SNS & SQS ready:")
print(f"Topic ARN: {topic_arn}")
print(f"Queue URL: {queue_url}")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_poll_project.settings')
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
