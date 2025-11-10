import os
import boto3

os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"

LOCALSTACK_URL = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

session = boto3.Session()
sns = session.client("sns", region_name=AWS_REGION, endpoint_url=LOCALSTACK_URL)

topics = sns.list_topics().get("Topics", [])
ms_names = []

for t in topics:
    topic_arn = t["TopicArn"]
    subs = sns.list_subscriptions_by_topic(TopicArn=topic_arn).get("Subscriptions", [])
    for s in subs:
        endpoint = s.get("Endpoint", "")
        if not endpoint:
            continue
        parts = endpoint.lower().split("prod")
        if len(parts) > 1 and parts[1]:
            ms_name = parts[1].strip("_-/")
        else:
            ms_name = endpoint.split("/")[-1].split(".")[0]
        if ms_name and ms_name not in ms_names:
            ms_names.append(ms_name)

print("🧩 Discovered subscriptions:", ms_names)

with open("discovered_microservices.txt", "w") as f:
    for name in ms_names:
        f.write(f"{name}\n")

print("✅ Saved discovered microservices to discovered_microservices.txt")
