import time, os
from pathlib import Path
from _parser import extract_resources
from _aws_helpers import init_aws_clients, aws_create_resource, create_aws_resources_batch
from _k8s_helpers import create_k8s_from_struct

DJANGO_SETTINGS_PATH = os.environ.get("DJANGO_SETTINGS_MODULE", "/app/my_poll_project/settings/dev.py")

def run_setup(settings_path=None):
    start = time.time()
    settings_path = settings_path or DJANGO_SETTINGS_PATH
    if not Path(settings_path).exists():
        print("❌ Settings not found.")
        return

    print(f"🔍 Scanning settings: {settings_path}")
    resources = extract_resources(settings_path)

    print("🔧 Initializing AWS clients...")
    boto_clients = init_aws_clients()
    
    if boto_clients is None:
        print("❌ Failed to initialize AWS clients")
        return

    created = {k: 0 for k in ('sqs', 'sns', 's3', 'lambda', 'dynamodb', 'events', 'k8s')}
    
    for service in ('sqs', 'sns', 's3', 'lambda', 'dynamodb', 'events'):
        resource_list = resources.get(service, [])
        if resource_list:
            print(f"🔄 Processing {service.upper()} resources...")
            for resource_name in resource_list:
                if isinstance(resource_name, str) and resource_name.startswith('arn:aws:'):
                    resource_name = resource_name.split(':')[-1]
                    
                if aws_create_resource(boto_clients, service, resource_name):
                    created[service] += 1

    if resources.get('k8s'):
        print("🧩 Handling K8s resources...")
        created['k8s'] = create_k8s_from_struct(resources['k8s']) if isinstance(resources['k8s'], dict) else 0

    print("\n🎉 Setup Summary:")
    print("=" * 40)
    total_created = 0
    for k, v in created.items():
        print(f" - {k.upper():12}: {v}")
        total_created += v
    
    print(f"\n📊 Total resources processed: {total_created}")
    print(f"⏱️  Elapsed time: {time.time()-start:.1f}s")

if __name__ == "__main__":
    import sys
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    run_setup(arg)