# polls/messaging/messaging_setup.py
from .clients import sns, sqs
import json

def create_topic(name):
    topic_arn = sns.create_topic(Name=name)["TopicArn"]
    print(f"✅ Topic created: {topic_arn}")
    return topic_arn

def create_queue(name, dlq_name=None):
    queue_url = sqs.create_queue(QueueName=name)["QueueUrl"]
    attrs = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=["QueueArn"])
    queue_arn = attrs["Attributes"]["QueueArn"]
    print(f"✅ Queue created: {queue_url}")

    dlq_arn = None
    if dlq_name:
        dlq_url = sqs.create_queue(QueueName=dlq_name)["QueueUrl"]
        dlq_attrs = sqs.get_queue_attributes(QueueUrl=dlq_url, AttributeNames=["QueueArn"])
        dlq_arn = dlq_attrs["Attributes"]["QueueArn"]

        redrive_policy = {
            "deadLetterTargetArn": dlq_arn,
            "maxReceiveCount": "3"
        }
        sqs.set_queue_attributes(
            QueueUrl=queue_url,
            Attributes={"RedrivePolicy": json.dumps(redrive_policy)}
        )
        print(f"🛑 DLQ attached: {dlq_url}")

    return {"url": queue_url, "arn": queue_arn, "dlq_arn": dlq_arn}

def attach_sns_policy(queue_arn, topic_arn, queue_url):
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": "*",
                "Action": "sqs:SendMessage",
                "Resource": queue_arn,
                "Condition": {"ArnEquals": {"aws:SourceArn": topic_arn}}
            }
        ]
    }
    sqs.set_queue_attributes(
        QueueUrl=queue_url,
        Attributes={"Policy": json.dumps(policy)}
    )
    print(f"🔑 Policy attached to {queue_url}")

def subscribe_queue(topic_arn, queue_arn, filter_policy=None):
    """Subscribe queue to SNS topic with optional filter policy."""
    params = {
        "TopicArn": topic_arn,
        "Protocol": "sqs",
        "Endpoint": queue_arn
    }
    if filter_policy:
        params["Attributes"] = {"FilterPolicy": json.dumps(filter_policy)}
    sns.subscribe(**params)
    print(f"🔗 Queue {queue_arn} subscribed to Topic {topic_arn} with filter {filter_policy}")

def setup_all():
    print("🚀 Starting messaging setup...")

    topics = {
        "question": create_topic("question-topic"),
        "choice": create_topic("choice-topic"),
        "user": create_topic("user-topic"),
        "stats": create_topic("stats-topic")
    }

    queues = {
        "question": create_queue("question-queue", dlq_name="question-dlq"),
        "choice": create_queue("choice-queue", dlq_name="choice-dlq"),
        "user": create_queue("user-queue", dlq_name="user-dlq"),
        "stats": create_queue("stats-queue", dlq_name="stats-dlq")
    }

    for q_key in queues:
        attach_sns_policy(queues[q_key]["arn"], topics[q_key], queues[q_key]["url"])


    subscribe_queue(
        topics["question"], queues["choice"]["arn"],
        filter_policy={"event_type": ["QUESTION_CREATED", "QUESTION_UPDATED"]}
    )
    subscribe_queue(
        topics["choice"], queues["choice"]["arn"],
        filter_policy={"event_type": ["QUESTION_CREATED", "QUESTION_UPDATED"]}
    )

    subscribe_queue(
        topics["choice"], queues["stats"]["arn"],
        filter_policy={"event_type": ["CHOICE_VOTED"]}
    )

    subscribe_queue(topics["question"], queues["question"]["arn"])
    subscribe_queue(topics["user"], queues["user"]["arn"])
    subscribe_queue(topics["stats"], queues["stats"]["arn"])

    print("🎉 Messaging setup completed successfully!")
    return {"topics": topics, "queues": queues}

if __name__ == "__main__":
    setup_all()
