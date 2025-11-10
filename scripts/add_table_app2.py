import os
import boto3
import mysql.connector

os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"

LOCALSTACK_URL = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3307, 
    user="dev_user",
    password="dev_pass"
)
cursor = conn.cursor()

session = boto3.Session()
sns = session.client("sns", region_name=AWS_REGION, endpoint_url=LOCALSTACK_URL)
sqs = session.client("sqs", region_name=AWS_REGION, endpoint_url=LOCALSTACK_URL)

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

print(f"🧩 Discovered microservices: {ms_names}")

num_tables = 10
num_columns = 8

for ms_name in ms_names:
    db_name = f"{ms_name}_db"
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
    print(f"✅ Database created: {db_name}")

    cursor.execute(f"USE `{db_name}`;")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS message_queue (
            id INT AUTO_INCREMENT PRIMARY KEY,
            queue_name VARCHAR(100),
            message_body TEXT,
            status ENUM('pending', 'processed', 'failed') DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    print(f"   ✅ Created table: message_queue")

    for i in range(1, num_tables + 1):
        table_name = f"data_table_{i}"
        columns = ["id INT AUTO_INCREMENT PRIMARY KEY"]
        for j in range(1, num_columns):
            columns.append(f"col_{j} VARCHAR(100)")
        columns_sql = ", ".join(columns)
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});")

    print(f"   ✅ Created {num_tables} extra tables for {db_name}")

conn.commit()
cursor.close()
conn.close()

print("🎉 All microservice databases created and linked to LocalStack successfully!")
