import os
import json
import time
from polls.messaging.clients import sqs

USER_QUEUE_URL = os.getenv("USER_QUEUE_URL")

def process_user_message(message):
    body = json.loads(message["Body"])
    if "Message" in body:
        body = json.loads(body["Message"])

    event_type = body.get("event")
    user_id = body.get("user_id")

    print(f"📩 User Event Received: {event_type} - {body}")

    if event_type == "USER_CREATED":
        print(f"✅ User Created: {user_id}")
    elif event_type == "USER_UPDATED":
        print(f"✏️ User Updated: {user_id}")
    elif event_type == "USER_DELETED":
        print(f"🗑️ User Deleted: {user_id}")
    else:
        print(f"⚠️ Unknown event type: {event_type}")

def consume_user_queue(wait_time=3, max_messages=5):
    print("🚀 Starting User queue consumer...")
    while True:
        response = sqs.receive_message(
            QueueUrl=USER_QUEUE_URL,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time,
            MessageAttributeNames=["All"]
        )

        for msg in response.get("Messages", []):
            try:
                process_user_message(msg)
                sqs.delete_message(
                    QueueUrl=USER_QUEUE_URL,
                    ReceiptHandle=msg["ReceiptHandle"]
                )
            except Exception as e:
                print(f"⚠️ Failed to process message: {msg.get('MessageId')} - {e}")
        time.sleep(1)
