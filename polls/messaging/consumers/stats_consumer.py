import json
import time
from polls.messaging.clients import sqs
from polls.services.stats_service import StatsService
from polls.models.database import Session
import os

STATS_QUEUE_URL = os.getenv("STATS_QUEUE_URL")  

def process_stats_message(message):
    """Process a single SQS message for stats updates."""
    try:
        body = json.loads(message.get("Body", "{}"))
        if "Message" in body: 
            body = json.loads(body["Message"])

        event = body.get("event")
        question_id = body.get("question_id")
        choice_id = body.get("choice_id")

        if event == "CHOICE_VOTED":
            print(f"📩 Received CHOICE_VOTED for Question {question_id}, Choice {choice_id}")

            votes = StatsService.get_question_votes(question_id)
            top_question = StatsService.get_top_question()
            top_choice = StatsService.get_top_choice()

            StatsService.list_questions_with_votes()

            print(f"📊 Stats updated for Question {question_id}: total votes = {votes}")
            print(f"🏆 Top Question: {top_question and top_question.get('question_text')}")
            print(f"🥇 Top Choice: {top_choice and top_choice.get('choice_text')}")

        Session.commit()

    except Exception as e:
        Session.rollback()
        print(f"⚠️ Failed to process stats message: {e}")
    finally:
        Session.remove()


def consume_stats_queue(wait_time=3, max_messages=5):
    """Continuously consume messages from the Stats queue."""
    print("🚀 Starting Stats queue consumer...")
    while True:
        response = sqs.receive_message(
            QueueUrl=STATS_QUEUE_URL,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time,
            MessageAttributeNames=["All"]
        )

        messages = response.get("Messages", [])
        for msg in messages:
            try:
                process_stats_message(msg)

                sqs.delete_message(
                    QueueUrl=STATS_QUEUE_URL,
                    ReceiptHandle=msg["ReceiptHandle"]
                )
            except Exception as e:
                print(f"⚠️ Failed to process or delete message: {e}")

        time.sleep(1)
