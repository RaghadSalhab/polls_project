# polls/messaging/core/setup_local_messaging.py
import logging
import json
from polls.messaging.core.clients import sqs, sns
from polls.messaging.core.config import MESSAGING_CONFIG
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

def queue_exists(queue_name):
    try:
        resp = sqs.list_queues(QueueNamePrefix=queue_name)
        urls = resp.get("QueueUrls", [])
        return any(queue_name in url for url in urls)
    except Exception:
        return False

def topic_exists(topic_name):
    try:
        resp = sns.list_topics()
        topics = resp.get("Topics", [])
        return any(topic_name in t["TopicArn"] for t in topics)
    except Exception:
        return False

def create_queue(queue_name):
    if not queue_exists(queue_name):
        sqs.create_queue(QueueName=queue_name)
        logger.info(f"✅ Queue created: {queue_name}")
        print(f"✅ Queue created: {queue_name}")
    else:
        logger.info(f"ℹ️ Queue already exists: {queue_name}")
        print(f"ℹ️ Queue already exists: {queue_name}")

def create_topic(topic_name):
    if not topic_exists(topic_name):
        resp = sns.create_topic(Name=topic_name)
        logger.info(f"✅ Topic created: {topic_name}")
        print(f"✅ Topic created: {topic_name}")
        return resp["TopicArn"]
    logger.info(f"ℹ️ Topic already exists: {topic_name}")
    print(f"ℹ️ Topic already exists: {topic_name}")
    return f"arn:aws:sns:us-east-1:000000000000:{topic_name}"

def subscribe_queue_to_topic(queue_name, topic_arn, filter_policy=None):
    # Get Queue ARN
    queue_url = f"http://localhost:4566/000000000000/{queue_name}"
    queue_attrs = sqs.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=["QueueArn"]
    )
    queue_arn = queue_attrs["Attributes"]["QueueArn"]

    # Attach policy
    policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": "*",
            "Action": "sqs:SendMessage",
            "Resource": queue_arn,
            "Condition": {"ArnEquals": {"aws:SourceArn": topic_arn}}
        }]
    }
    sqs.set_queue_attributes(
        QueueUrl=queue_url,
        Attributes={"Policy": json.dumps(policy)}
    )

    # Check if subscription exists
    existing_subs = sns.list_subscriptions_by_topic(TopicArn=topic_arn)["Subscriptions"]
    for sub in existing_subs:
        if sub["Endpoint"] == queue_arn:
            logger.info(f"🔗 Subscription already exists: {topic_arn} → {queue_arn}")
            return

    # Create subscription
    params = {
        "TopicArn": topic_arn,
        "Protocol": "sqs",
        "Endpoint": queue_arn
    }
    if filter_policy:
        params["Attributes"] = {"FilterPolicy": json.dumps(filter_policy)}

    sns.subscribe(**params)
    logger.info(f"🔗 Subscription created: {topic_arn} → {queue_arn}")

def run_setup():
    logger.info("🚀 Running local messaging setup from MESSAGING_CONFIG...")

    for service_name, topic_cfg in MESSAGING_CONFIG.items():
        topic_arn = create_topic(topic_cfg.name)

        for queue_cfg in topic_cfg.queues:
            create_queue(queue_cfg.name)
            if queue_cfg.dlq_name:
                create_queue(queue_cfg.dlq_name)

            subscribe_queue_to_topic(
                queue_name=queue_cfg.name,
                topic_arn=topic_arn,
                filter_policy=queue_cfg.filter_policy
            )

    logger.info("🎉 Local messaging setup completed successfully!")
    print("🎉 Local messaging setup completed successfully!")
