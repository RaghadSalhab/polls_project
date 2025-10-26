#!/usr/bin/env python3

# scripts/_00_smart_env_setup.py
"""
Smart environment setup:
- Structured parsing (ast) for keys like AWS, K8S, REDIS, POSTGRES
- Heuristic regex scanning for scattered resources (prod-, dev-, queue, topic, s3://, arn:aws:sns, function, redis://, postgres://, k8s, deployment, service)
- Creation on LocalStack (AWS), kubectl apply (K8s), docker run suggestions for Redis/Postgres (optional execution).
"""

import os
import ast
import re
import json
import time
import socket
import subprocess
from pathlib import Path

# ---------- Configuration ----------
DJANGO_SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE", "my_poll_project.settings.dev")
LOCALSTACK_ENDPOINT = os.environ.get("LOCALSTACK_ENDPOINT", "http://localhost:4566")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", "test")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", "test")
AWS_DEFAULT_REGION = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
DOCKER_AUTO_START = True
KUBECTL_AUTO_APPLY = os.environ.get("KUBECTL_AUTO_APPLY", "true").lower() == "true"  # apply generated k8s yamls if kubectl present

# ---------- Optional imports for AWS clients (lazy) ----------
def import_boto3():
    try:
        import boto3
        return boto3
    except Exception:
        return None

# ---------- Utilities ----------
def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
from pathlib import Path
from pathlib import Path

def find_settings_file(possible_paths=None):
    if possible_paths is None:
        # كل ملفات settings الممكنة
        possible_paths = list(Path("/app/my_poll_project/settings").glob("*.py"))
    for p in possible_paths:
        if Path(p).exists():
            return str(p)
    return None

# ---------- AST structured parsing ----------
def parse_structured_resources(path):
    """
    Parse top-level assignments like AWS = {...}, K8S = {...}, REDIS = {...}
    Return dict: {'aws': {...}, 'k8s': {...}, 'redis': {...}, 'postgres': {...}}
    """
    content = read_file(path)
    tree = ast.parse(content)
    found = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    name = target.id.upper()
                    try:
                        value = ast.literal_eval(node.value)
                    except Exception:
                        # Couldn't evaluate statically (could be computed) => skip
                        value = None
                    if value is not None:
                        found[name] = value
    return found

def deep_extract_values(obj):
    """Recursively extract str values from dicts/lists/tuples"""
    results = []
    if isinstance(obj, dict):
        for v in obj.values():
            results.extend(deep_extract_values(v))
    elif isinstance(obj, (list, tuple, set)):
        for v in obj:
            results.extend(deep_extract_values(v))
    elif isinstance(obj, str):
        results.append(obj)
    return results

# ---------- Regex heuristic parsing (unstructured) ----------
UNSTRUCTURED_PATTERNS = {
    'sqs': [
        r'["\']([a-zA-Z0-9\-_]+queue[a-zA-Z0-9\-_]*)["\']',
        r'["\']((?:prod|dev|staging)-[a-zA-Z0-9\-_]+)["\']',
        r'["\']([a-zA-Z0-9\-_]+updates[a-zA-Z0-9\-_]*)["\']',
    ],
    'sns': [
        r'arn:aws:sns:[^"\']*:([^"\']+)',
        r'["\']([a-zA-Z0-9\-_]+(?:topic|notification)[a-zA-Z0-9\-_]*)["\']',
    ],
    's3': [
        r'["\']([a-zA-Z0-9\-_]+(?:bucket)[a-zA-Z0-9\-_]*)["\']',
        r's3://([a-zA-Z0-9\-_]+)',
    ],
    'lambda': [
        r'["\']([a-zA-Z0-9\-_]+(?:function)[a-zA-Z0-9\-_]*)["\']',
        r'arn:aws:lambda:[^"\']*:function:([^"\']+)',
    ],
    'k8s': [
        r'["\'](k8s[-_a-zA-Z0-9]+)["\']',
        r'\b(deployment|service|ingress|pod|cronjob)\b',
    ],
    'redis': [
        r'redis://',
        r'["\']REDIS["\']',
    ]
}

def heuristic_scan(content):
    found = {'sqs': set(), 'sns': set(), 's3': set(), 'lambda': set(), 'k8s': set(), 'db': set(), 'redis': set(), 'other_arns': set()}
    # full arns for any service
    arns = re.findall(r'arn:aws:[^"\']+', content)
    for arn in arns:
        if ':sns:' in arn:
            found['sns'].add(arn.split(':')[-1])
        elif ':lambda:' in arn:
            found['lambda'].add(arn.split(':')[-1])
        else:
            found['other_arns'].add(arn)

    for svc, pats in UNSTRUCTURED_PATTERNS.items():
        for pat in pats:
            matches = re.findall(pat, content, re.IGNORECASE)
            for m in matches:
                if isinstance(m, tuple):
                    m = m[0]
                found.setdefault(svc, set()).add(m)
    return found

# ---------- AWS helpers (LocalStack) ----------
def init_aws_clients():
    boto3 = import_boto3()
    if boto3 is None:
        print("⚠️ boto3 not installed. AWS creation will be skipped.")
        return None
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION
    )
    clients = {
        'sqs': session.client('sqs', endpoint_url=LOCALSTACK_ENDPOINT),
        'sns': session.client('sns', endpoint_url=LOCALSTACK_ENDPOINT),
        's3': session.client('s3', endpoint_url=LOCALSTACK_ENDPOINT),
        'lambda': session.client('lambda', endpoint_url=LOCALSTACK_ENDPOINT),
    }
    return clients

def aws_resource_exists(clients, service, name):
    try:
        if service == 'sqs':
            urls = clients['sqs'].list_queues().get('QueueUrls', []) or []
            return any(name in q for q in urls)
        if service == 'sns':
            topics = [t['TopicArn'].split(':')[-1] for t in clients['sns'].list_topics().get('Topics', [])]
            return name in topics
        if service == 's3':
            buckets = [b['Name'] for b in clients['s3'].list_buckets().get('Buckets', [])]
            return name in buckets
        if service == 'lambda':
            funcs = [f['FunctionName'] for f in clients['lambda'].list_functions().get('Functions', [])]
            return name in funcs
    except Exception as e:
        print(f"⚠️ AWS existence check error for {service}/{name}: {e}")
    return False

def aws_create_resource(clients, service, name):
    if clients is None:
        print(f"⚠️ Skipping {service} creation (boto3 not available): {name}")
        return False
    clean = re.sub(r'[^a-zA-Z0-9\-_\.]', '-', name).lower() if service == 's3' else re.sub(r'[^a-zA-Z0-9\-_]', '-', name)
    if aws_resource_exists(clients, service, clean):
        print(f"ℹ️ AWS {service} exists: {clean}")
        return False
    try:
        if service == 'sqs':
            clients['sqs'].create_queue(QueueName=clean)
        elif service == 'sns':
            clients['sns'].create_topic(Name=clean)
        elif service == 's3':
            clients['s3'].create_bucket(Bucket=clean)
        elif service == 'lambda':
            clients['lambda'].create_function(
                FunctionName=clean,
                Runtime='python3.9',
                Role='arn:aws:iam::000000000000:role/lambda-role',
                Handler='lambda_function.lambda_handler',
                Code={'ZipFile': b'def lambda_handler(e,c): return {}'}
            )
        print(f"✅ Created AWS {service}: {clean}")
        return True
    except Exception as e:
        print(f"❌ Failed to create AWS {service} {name}: {e}")
        return False

# ---------- Kubernetes helpers ----------
def kubectl_available():
    try:
        subprocess.run(['kubectl', 'version', '--client'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

def apply_k8s_yaml(yaml_content, name_hint="auto"):
    tmp = Path(f"/tmp/smart-k8s-{name_hint}.yaml")
    tmp.write_text(yaml_content, encoding='utf-8')
    if KUBECTL_AUTO_APPLY and kubectl_available():
        try:
            subprocess.run(['kubectl', 'apply', '-f', str(tmp)], check=True)
            print(f"✅ Applied k8s YAML: {tmp}")
            return True
        except Exception as e:
            print(f"❌ kubectl apply failed: {e} - YAML written at {tmp}")
            return False
    else:
        print(f"ℹ️ kubectl not available or auto-apply disabled. YAML written to {tmp}")
        return False

def create_k8s_from_struct(k8s_obj):
    """
    Expect k8s_obj like {'SERVICES': [...], 'DEPLOYMENTS': [...]}
    For each create a basic YAML and apply.
    """
    created = 0
    if not isinstance(k8s_obj, dict):
        return created
    svcs = k8s_obj.get('SERVICES') or k8s_obj.get('services') or []
    deps = k8s_obj.get('DEPLOYMENTS') or k8s_obj.get('deployments') or []
    for svc in svcs:
        name = svc.get('name') if isinstance(svc, dict) else str(svc)
        port = svc.get('port', 80) if isinstance(svc, dict) else 80
        yaml = f"""
apiVersion: v1
kind: Service
metadata:
  name: {name}
spec:
  selector:
    app: {name}
  ports:
    - protocol: TCP
      port: {port}
      targetPort: {port}
"""
        if apply_k8s_yaml(yaml, name_hint=name):
            created += 1
    for dep in deps:
        name = dep.get('name') if isinstance(dep, dict) else str(dep)
        replicas = dep.get('replicas', 1) if isinstance(dep, dict) else 1
        image = dep.get('image', 'nginx:latest') if isinstance(dep, dict) else 'nginx:latest'
        yaml = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {name}
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {name}
  template:
    metadata:
      labels:
        app: {name}
    spec:
      containers:
      - name: {name}-container
        image: {image}
        ports:
        - containerPort: 80
"""
        if apply_k8s_yaml(yaml, name_hint=name):
            created += 1
    return created

# ---------- Database/Redis helpers ----------
def is_port_open(host, port, timeout=1.0):
    try:
        with socket.create_connection((host, int(port)), timeout=timeout):
            return True
    except Exception:
        return False

def ensure_redis(host='localhost', port=6379):
    if is_port_open(host, port):
        print(f"ℹ️ Redis already listening at {host}:{port}")
        return False
    cmd = f"docker run -d --name smart_redis -p {port}:6379 redis:7-alpine"
    print(f"ℹ️ Redis not found on {host}:{port}. Suggested command:\n   {cmd}")
    if DOCKER_AUTO_START:
        try:
            subprocess.run(cmd.split(), check=True)
            print("✅ Redis container started")
            return True
        except Exception as e:
            print(f"❌ Failed to start Redis container: {e}")
    return False

def ensure_postgres(host='localhost', port=5432):
    if is_port_open(host, port):
        print(f"ℹ️ Postgres already listening at {host}:{port}")
        return False
    cmd = f"docker run -d --name smart_postgres -e POSTGRES_PASSWORD=postgres -p {port}:5432 postgres:15-alpine"
    print(f"ℹ️ Postgres not found on {host}:{port}. Suggested command:\n   {cmd}")
    if DOCKER_AUTO_START:
        try:
            subprocess.run(cmd.split(), check=True)
            print("✅ Postgres container started")
            return True
        except Exception as e:
            print(f"❌ Failed to start Postgres container: {e}")
    return False

# ---------- Main orchestration ----------
def run_setup(settings_path=None):
    start = time.time()
    settings_path = settings_path or find_settings_file()
    if not settings_path:
        print("❌ Could not find settings file. Put path as argument or create expected settings files.")
        return

    print(f"🔍 Scanning settings: {settings_path}")
    content = read_file(settings_path)

    # 1) Structured parse using AST
    structured = parse_structured_resources(settings_path)
    resources = {'sqs': set(), 'sns': set(), 's3': set(), 'lambda': set(), 'k8s': set(), 'db': set(), 'redis': set(), 'other_arns': set()}

    # If AWS dict present, extract nested values
    if 'AWS' in structured:
        aws = structured['AWS']
        # for each key under AWS, collect string values deeply
        for svc_key, svc_val in aws.items():
            k = svc_key.lower()
            vals = deep_extract_values(svc_val)
            if k in ('sqs','sns','s3','lambda'):
                resources[k].update(vals)
            else:
                # If it's an ARN or unknown service, check ARNs
                for v in vals:
                    if isinstance(v, str) and v.startswith('arn:aws:'):
                        if ':sns:' in v:
                            resources['sns'].add(v.split(':')[-1])
                        elif ':lambda:' in v:
                            resources['lambda'].add(v.split(':')[-1])
                        else:
                            resources['other_arns'].add(v)

    # If K8S/ K8s / K8S present structured
    if 'K8S' in structured or 'K8s' in structured or 'k8s' in structured:
        k8s_key = 'K8S' if 'K8S' in structured else ('K8s' if 'K8s' in structured else 'k8s')
        resources['k8s'] = structured[k8s_key]

    # If REDIS or POSTGRES structured
    if 'REDIS' in structured:
        resources['redis'].update(deep_extract_values(structured['REDIS']))
    if 'POSTGRES' in structured or 'DATABASES' in structured:
        # DATABASES might be a Django DB dict
        if 'POSTGRES' in structured:
            resources['db'].update(deep_extract_values(structured['POSTGRES']))
        if 'DATABASES' in structured:
            # try to find default conn string or host/port
            dbvals = deep_extract_values(structured['DATABASES'])
            resources['db'].update(dbvals)

    # 2) Heuristic unstructured scan (fallback/network)
    heur = heuristic_scan(content)
    for k, v in heur.items():
        if k in resources:
            resources[k].update(v)
        else:
            resources['other_arns'].update(v if isinstance(v, set) else {v})

    # Summarize detected
    print("\n📊 Detected resources summary:")
    for k, v in resources.items():
        try:
            count = len(v) if hasattr(v, '__len__') else (len(deep_extract_values(v)) if isinstance(v, (dict,list)) else 0)
        except Exception:
            count = 1
        print(f" - {k.upper():8}: {count}")

    # 3) Create / ensure resources
    created = {'sqs':0,'sns':0,'s3':0,'lambda':0,'k8s':0,'redis':0,'db':0}
    boto_clients = init_aws_clients()

    # AWS resources
    for svc in ('sqs','sns','s3','lambda'):
        items = resources.get(svc, [])
        for it in items:
            # clean string: if ARN passed, pick last part
            if isinstance(it, str) and it.startswith('arn:aws:'):
                it = it.split(':')[-1]
            success = aws_create_resource(boto_clients, svc, it)
            if success:
                created[svc] += 1

    # K8s resources
    if resources.get('k8s'):
        print("\n🧩 Handling Kubernetes resources...")
        created_k8s = create_k8s_from_struct(resources['k8s']) if isinstance(resources['k8s'], dict) else 0
        created['k8s'] = created_k8s

    # Redis/Postgres
    # Try to detect host/port pairs from structured or defaults
    # If structured REDIS provided as dict, extract host/port
    redis_created = False
    if 'REDIS' in structured and isinstance(structured['REDIS'], dict):
        host = structured['REDIS'].get('HOST','localhost')
        port = structured['REDIS'].get('PORT',6379)
        redis_created = ensure_redis(host=host, port=port)
    else:
        # fallback: check default localhost:6379 if heuristics found any redis mention
        if resources.get('redis'):
            redis_created = ensure_redis('localhost', 6379)
    created['redis'] = 1 if redis_created else 0

    db_created = False
    if 'POSTGRES' in structured and isinstance(structured['POSTGRES'], dict):
        host = structured['POSTGRES'].get('HOST','localhost')
        port = structured['POSTGRES'].get('PORT',5432)
        db_created = ensure_postgres(host=host, port=port)
    else:
        # check DATABASES default guess
        if resources.get('db'):
            db_created = ensure_postgres('localhost', 5432)
    created['db'] = 1 if db_created else 0

    # Final summary
    print("\n🎉 Setup done. Summary of creations:")
    for k,v in created.items():
        print(f"  - {k.upper():12}: {v}")

    print(f"\nElapsed: {time.time()-start:.1f}s")
    print("Tip: To run this automatically with LocalStack, place this script in the container's ready.d folder or mount it via docker-compose volume.")

# ---------- CLI ----------
if __name__ == "__main__":
    import sys
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    run_setup(arg)
