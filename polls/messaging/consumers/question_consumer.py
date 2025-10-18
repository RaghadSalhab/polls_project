import json
import time
from polls.messaging.clients import sqs
from polls.repositories.question_repository import QuestionRepository
from polls.models.database import Session
import os

QUESTION_QUEUE_URL = os.getenv("QUESTION_QUEUE_URL")


def process_question_message(message):

    body = json.loads(message["Body"])
    if "Message" in body:
        body = json.loads(body["Message"])

    event_type = body.get("event")
    print(f"📩 Question Event Received: {event_type} - {body}")

    question_id = body.get("question_id")
    user_id = body.get("user_id")

    if event_type == "QUESTION_CREATED":
        question = QuestionRepository.get(question_id)
        if not question:
            question = QuestionRepository.add(
                QuestionRepository.model(
                    id=question_id,
                    created_by_id=user_id,
                    question_text=body.get("question_text")
                )
            )
        print(f"✅ Question Created: {question.id} by User {user_id}")

    elif event_type == "QUESTION_UPDATED":
        question = QuestionRepository.get(question_id)
        if question:
            question.question_text = body.get("question_text")
            Session.commit()
            print(f"✏️ Question Updated: {question.id} by User {user_id}")
        else:
            print(f"⚠️ Question {question_id} not found for update")

    elif event_type == "QUESTION_DELETED":
        deleted = QuestionRepository.delete_by_id(question_id, commit=True)
        if deleted:
            print(f"🗑️ Question Deleted: {question_id}")
        else:
            print(f"⚠️ Question {question_id} not found for deletion")

    else:
        print(f"⚠️ Unknown event type: {event_type}")


def consume_question_queue(wait_time=3, max_messages=5):
    print("🚀 Starting Question queue consumer...")
    while True:
        response = sqs.receive_message(
            QueueUrl=QUESTION_QUEUE_URL,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time,
            MessageAttributeNames=["All"]
        )
        messages = response.get("Messages", [])
        for msg in messages:
            try:
                process_question_message(msg)
                sqs.delete_message(
                    QueueUrl=QUESTION_QUEUE_URL,
                    ReceiptHandle=msg["ReceiptHandle"]
                )
            except Exception as e:
                print(f"⚠️ Failed to process message: {msg.get('MessageId')} - {e}")
        time.sleep(1)
