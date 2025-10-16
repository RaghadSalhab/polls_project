
import boto3
import os
import json
import time

QUEUE_URL = os.getenv("QUEUE_URL", "http://localhost:4566/000000000000/QuestionQueue")

sqs = boto3.client(
    "sqs",
    endpoint_url=os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
)

print(f"Listening for messages on {QUEUE_URL}... (Ctrl+C to stop)")

while True:
    resp = sqs.receive_message(
        QueueUrl=QUEUE_URL,
        MaxNumberOfMessages=1,
        WaitTimeSeconds=5
    )

    messages = resp.get("Messages", [])
    if not messages:
        continue

    for msg in messages:
        body = msg.get("Body", "")
        
        # Parsing JSON inside JSON
        try:
            msg_json = json.loads(body)
            if "Message" in msg_json:
                payload = json.loads(msg_json["Message"])
                print(f"📩 New Question Event: {payload}")
            else:
                print(f"Raw message: {msg_json}")
        except json.JSONDecodeError:
            print(f"Received text message: {body}")

        # Delete after processing
        sqs.delete_message(
            QueueUrl=QUEUE_URL,
            ReceiptHandle=msg["ReceiptHandle"]
        )
