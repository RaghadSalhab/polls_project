# _aws_helpers.py
import re

def import_boto3():
    try:
        import boto3
        return boto3
    except Exception:
        return None
    
# initialize boto3 clients for localstack or specified endpoint
def init_aws_clients(endpoint="http://localhost:4566", access_key="test", secret_key="test", region="us-east-1"):
    boto3 = import_boto3()
    if boto3 is None:
        print("⚠️ boto3 not installed.")
        return None
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    clients = {s: session.client(s, endpoint_url=endpoint) for s in ('sqs','sns','s3','lambda')}
    return clients

# check if an AWS resource exists by listing existing resources of that type and checking for the name 
def aws_resource_exists(clients, service, name):
    try:
        if service=='sqs': urls = clients['sqs'].list_queues().get('QueueUrls', [])
        if service=='sns': urls = [t['TopicArn'].split(':')[-1] for t in clients['sns'].list_topics().get('Topics',[])]
        if service=='s3': urls = [b['Name'] for b in clients['s3'].list_buckets().get('Buckets',[])]
        if service=='lambda': urls = [f['FunctionName'] for f in clients['lambda'].list_functions().get('Functions',[])]
        return name in urls
    except Exception: return False

# create an AWS resource if it does not already exist
def aws_create_resource(clients, service, name):
    if clients is None: return False
    clean = re.sub(r'[^a-zA-Z0-9\-_\.]', '-', name).lower() if service=='s3' else re.sub(r'[^a-zA-Z0-9\-_]', '-', name)
    if aws_resource_exists(clients, service, clean):
        print(f"ℹ️ AWS {service} exists: {clean}")
        return False
    try:
        if service=='sqs': clients['sqs'].create_queue(QueueName=clean)
        elif service=='sns': clients['sns'].create_topic(Name=clean)
        elif service=='s3': clients['s3'].create_bucket(Bucket=clean)
        elif service=='lambda': print(f"ℹ️ Lambda creation skipped: {clean}")
        print(f"✅ Created AWS {service}: {clean}")
        return True
    except Exception as e:
        print(f"❌ Failed to create AWS {service} {name}: {e}")
        return False
