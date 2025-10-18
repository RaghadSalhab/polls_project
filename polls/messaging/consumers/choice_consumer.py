import json
import time
import uuid
from polls.models.request_scope import set_current_request
from polls.models.database import Session
from polls.services.choice_service import ChoiceService
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from polls.messaging.clients import sqs
import os

CHOICE_QUEUE_URL = os.getenv("CHOICE_QUEUE_URL")

class FakeRequest:
    """Fake request object to use with scoped_session."""
    def __init__(self):
        self.id = str(uuid.uuid4())

def process_choice_message(message):
    request = FakeRequest()
    set_current_request(request)

    try:
        body = json.loads(message.get("Body", "{}"))
        if "Message" in body:
            body = json.loads(body["Message"])

        event_type = body.get("event")
        user_id = body.get("user_id")
        question_id = body.get("question_id")

        if event_type in ["QUESTION_CREATED", "QUESTION_UPDATED"]:
            choices = body.get("choices", [])
            normalized_choices = []
            for c in choices:
                if isinstance(c, str):
                    normalized_choices.append({"choice_text": c})
                else:
                    normalized_choices.append(c)

            existing_choices = ChoiceService.list_choices_for_question(question_id)
            existing_texts = {c['choice_text']: c['id'] for c in existing_choices}

            for choice_data in normalized_choices:
                choice_text = choice_data.get("choice_text")
                choice_id = choice_data.get("id") or existing_texts.get(choice_text)

                try:
                    if choice_id:
                        choice = ChoiceService.update_choice(user_id, choice_id, choice_text)
                        print(f"✏️ Choice Updated (from question event): {choice['id']}")
                    else:
                        choice = ChoiceService.create_choice(user_id, question_id, choice_text)
                        print(f"✅ Choice Created (from question event): {choice['id']}")
                except Exception as e:
                    print(f"⚠️ Choice processing failed for '{choice_text}': {e}")
       
    except (ObjectDoesNotExist, PermissionDenied) as e:
        Session.rollback()
        print(f"⚠️ Business rule violation: {e}")
    except Exception as e:
        Session.rollback()
        print(f"⚠️ Failed to process message: {e}")
    finally:
        Session.remove()

def consume_choice_queue(wait_time=3, max_messages=5):
    print("🚀 Starting Choice queue consumer...")
    while True:
        response = sqs.receive_message(
            QueueUrl=CHOICE_QUEUE_URL,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time,
            MessageAttributeNames=["All"]
        )
        messages = response.get("Messages", [])
        for msg in messages:
            try:
                process_choice_message(msg)
                sqs.delete_message(
                    QueueUrl=CHOICE_QUEUE_URL,
                    ReceiptHandle=msg["ReceiptHandle"]
                )
            except Exception as e:
                print(f"⚠️ Failed to process message: {msg.get('MessageId')} - {e}")
        time.sleep(1)
