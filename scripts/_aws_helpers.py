import re
import time

def import_boto3():
    try:
        import boto3
        return boto3
    except Exception:
        return None

def is_valid_resource_name(service, name):
    if not name or not isinstance(name, str):
        return False
        
    validation_rules = {
        's3': (3, 63, r'^[a-z0-9.-]+$'),  # S3 bucket names
        'sqs': (1, 80, r'^[a-zA-Z0-9_-]+$'),  # SQS queue names
        'sns': (1, 256, r'^[a-zA-Z0-9_-]+$'),  # SNS topic names
        'dynamodb': (3, 255, r'^[a-zA-Z0-9_.-]+$'),  # DynamoDB table names
        'lambda': (1, 64, r'^[a-zA-Z0-9_-]+$'),  # Lambda function names
        'events': (1, 64, r'^[a-zA-Z0-9_-]+$'),  # EventBridge rule names
    }
    
    if service not in validation_rules:
        return True 
        
    min_len, max_len, pattern = validation_rules[service]
    
    if len(name) < min_len or len(name) > max_len:
        print(f"❌ Invalid {service} name length: {name} (must be {min_len}-{max_len} chars)")
        return False
        
    if not re.match(pattern, name):
        print(f"❌ Invalid {service} name format: {name}")
        return False
        
    return True

def aws_resource_exists(clients, service, name):
    try:
        if service == 'sqs': 
            urls = clients['sqs'].list_queues().get('QueueUrls', [])
            queue_names = [url.split('/')[-1] for url in urls]
            return name in queue_names
            
        elif service == 'sns': 
            topics = clients['sns'].list_topics().get('Topics', [])
            topic_names = [t['TopicArn'].split(':')[-1] for t in topics]
            return name in topic_names
            
        elif service == 's3': 
            buckets = clients['s3'].list_buckets().get('Buckets', [])
            bucket_names = [b['Name'] for b in buckets]
            return name in bucket_names
            
        elif service == 'dynamodb':
            tables = clients['dynamodb'].list_tables().get('TableNames', [])
            return name in tables
            
        elif service == 'lambda':
            functions = clients['lambda'].list_functions().get('Functions', [])
            function_names = [f['FunctionName'] for f in functions]
            return name in function_names
            
        elif service == 'events':
            rules = clients['events'].list_rules().get('Rules', [])
            rule_names = [r['Name'] for r in rules]
            return name in rule_names
            
    except Exception as e:
        print(f"⚠️ Error checking if {service} {name} exists: {e}")
        return False
        
    return False

def get_sqs_attributes(name, context=None):
    attributes = {
        'DelaySeconds': '0',
        'VisibilityTimeout': '30',
        'ReceiveMessageWaitTimeSeconds': '0'
    }
    
    name_lower = name.lower()
    
    if 'deadletter' in name_lower or 'dlq' in name_lower:
        attributes['MessageRetentionPeriod'] = '1209600'  
        print(f"   ↳ DLQ detected, setting 14-day retention")
        
    if 'notification' in name_lower or 'alert' in name_lower:
        attributes['VisibilityTimeout'] = '60'
        
    if 'batch' in name_lower or 'processing' in name_lower:
        attributes['VisibilityTimeout'] = '300'
        attributes['ReceiveMessageWaitTimeSeconds'] = '20'
        
    return attributes

def get_sns_attributes(name, context=None):
    attributes = {}
    
    name_lower = name.lower()
    
    if 'notification' in name_lower or 'alert' in name_lower:
        attributes['DisplayName'] = name.replace('-', ' ').title()
        
    return attributes

def get_dynamodb_config(name, context=None):
    return {
        'TableName': name,
        'KeySchema': [
            {'AttributeName': 'id', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        'BillingMode': 'PAY_PER_REQUEST',
        'Tags': [
            {'Key': 'Environment', 'Value': 'dev'},
            {'Key': 'CreatedBy', 'Value': 'smart-env-setup'}
        ]
    }

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
    
    services = [
        'sqs', 'sns', 's3', 'lambda', 
        'dynamodb', 'cloudwatch', 'events', 
        'stepfunctions', 'logs', 'kinesis'
    ]
    
    clients = {}
    for service in services:
        try:
            clients[service] = session.client(service, endpoint_url=endpoint)
            print(f"✅ Initialized {service} client")
        except Exception as e:
            print(f"⚠️ Skipping {service} client: {e}")
    
    return clients

def aws_create_resource(clients, service, name, max_retries=3, context=None):
    if clients is None:
        print("❌ AWS clients not initialized")
        return False
        
    if service not in clients:
        print(f"❌ Service {service} not supported or client not available")
        return False
        
    if not is_valid_resource_name(service, name):
        print(f"❌ Invalid {service} name: {name}")
        return False
        
    if aws_resource_exists(clients, service, name):
        print(f"✅ {service.upper()} already exists: {name}")
        return True
        
    for attempt in range(max_retries):
        try:
            if service == 'sqs':
                attributes = get_sqs_attributes(name, context)
                clients['sqs'].create_queue(QueueName=name, Attributes=attributes)
                
            elif service == 'sns':
                attributes = get_sns_attributes(name, context)
                clients['sns'].create_topic(Name=name, Attributes=attributes)
                
            elif service == 's3':
                clients['s3'].create_bucket(Bucket=name)
                
            elif service == 'dynamodb':
                table_config = get_dynamodb_config(name, context)
                clients['dynamodb'].create_table(**table_config)
                
            elif service == 'lambda':
                print(f"⏭️ Lambda creation requires code package: {name}")
                return False
                
            elif service == 'events':
                clients['events'].put_rule(
                    Name=name,
                    State='ENABLED',
                    Description=f"Auto-created rule for {name}"
                )
                
            elif service == 'stepfunctions':
                definition = {
                    "Comment": f"Simple state machine for {name}",
                    "StartAt": "HelloWorld",
                    "States": {
                        "HelloWorld": {
                            "Type": "Pass",
                            "Result": "Hello World!",
                            "End": True
                        }
                    }
                }
                clients['stepfunctions'].create_state_machine(
                    name=name,
                    definition=str(definition),
                    roleArn="arn:aws:iam::000000000000:role/localstack"
                )
                
            elif service == 'logs':
                clients['logs'].create_log_group(logGroupName=name)
                
            elif service == 'kinesis':
                clients['kinesis'].create_stream(StreamName=name, ShardCount=1)
                
            else:
                print(f"⏭️ Basic creation not implemented for {service}: {name}")
                return False
                
            print(f"✅ Created {service.upper()}: {name}")
            return True
            
        except Exception as e:
            if attempt == max_retries - 1: 
                print(f"❌ Failed to create {service} '{name}' after {max_retries} attempts: {e}")
                return False
            else:
                print(f"⚠️ Retry {attempt + 1}/{max_retries} for {service} '{name}'...")
                time.sleep(1)  
    
    return False

def create_aws_resources_batch(clients, resources_dict):
    results = {
        'success': 0,
        'failed': 0,
        'skipped': 0,
        'details': []
    }
    
    for service, resource_list in resources_dict.items():
        if service not in ['sqs', 'sns', 's3', 'dynamodb', 'lambda', 'events']:
            continue
            
        for resource_name in resource_list:
            if aws_create_resource(clients, service, resource_name):
                results['success'] += 1
                results['details'].append(f"✅ {service.upper()}: {resource_name}")
            else:
                results['failed'] += 1
                results['details'].append(f"❌ {service.upper()}: {resource_name}")
    
    return results