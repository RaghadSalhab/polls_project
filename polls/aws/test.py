import os
import json
import boto3

topic_arn = "arn:aws:sns:us-east-1:000000000000:QuestionEvents"

sns = boto3.client(
    "sns",
    region_name="us-east-1",
    endpoint_url=os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566"),
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

sns.publish(
    TopicArn=topic_arn,
    Message=json.dumps({"event": "TEST_MESSAGE", "text": "Hello from host"})
)

print("✅ Test message sent!")
