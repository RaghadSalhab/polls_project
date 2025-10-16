# polls/aws/setup_localstack.py
import boto3
import os

#endpoint = "http://localhost:4566" for localstack 
endpoint = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
region = "us-east-1"

# --- Initialize sns and sqs clients ---
sns = boto3.client(
    "sns",
    region_name=region,
    endpoint_url=endpoint,
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

sqs = boto3.client(
    "sqs",
    region_name=region,
    endpoint_url=endpoint,
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

TOPIC_NAME = "QuestionEvents"
QUEUE_NAME = "QuestionQueue"

# --- Create or get SNS Topic ---
existing_topics = sns.list_topics()["Topics"]
topic_arn = None
for t in existing_topics:
    if t["TopicArn"].endswith(":" + TOPIC_NAME):
        topic_arn = t["TopicArn"]
        print(f"✅ Topic already exists: {topic_arn}")
        break

if not topic_arn:
    topic = sns.create_topic(Name=TOPIC_NAME)
    topic_arn = topic["TopicArn"]
    print(f"✅ Topic created: {topic_arn}")

# --- Create or get SQS Queue ---
existing_queues = sqs.list_queues().get("QueueUrls", [])
queue_url = None
for q in existing_queues:
    if q.endswith("/" + QUEUE_NAME):
        queue_url = q
        print(f"✅ Queue already exists: {queue_url}")
        break

if not queue_url:
    queue = sqs.create_queue(QueueName=QUEUE_NAME)
    queue_url = queue["QueueUrl"]
    print(f"✅ Queue created: {queue_url}")

# --- Get Queue ARN ---
queue_arn = sqs.get_queue_attributes(
    QueueUrl=queue_url,
    AttributeNames=["QueueArn"]
)["Attributes"]["QueueArn"]

# --- Subscribe Queue to Topic (if not already subscribed) ---
subs = sns.list_subscriptions_by_topic(TopicArn=topic_arn)["Subscriptions"]
already_subscribed = any(sub["Endpoint"] == queue_arn for sub in subs)

if not already_subscribed:
    sns.subscribe(TopicArn=topic_arn, Protocol="sqs", Endpoint=queue_arn)
    print(f"✅ Queue subscribed to topic: {queue_arn} -> {topic_arn}")
else:
    print(f"✅ Queue already subscribed to topic")

print("🎉 LocalStack setup complete")
