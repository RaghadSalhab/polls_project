import boto3
import os

AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
LOCALSTACK_ENDPOINT = os.getenv("LOCALSTACK_ENDPOINT", "http://localstack:4566") 

sns = boto3.client(
    "sns",
    region_name=AWS_REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test",
    endpoint_url=LOCALSTACK_ENDPOINT
)

sqs = boto3.client(
    "sqs",
    region_name=AWS_REGION,
    aws_access_key_id="test",
    aws_secret_access_key="test",
    endpoint_url=LOCALSTACK_ENDPOINT
)
