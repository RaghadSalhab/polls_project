# _00_smart_env_setup.py
import time, os
from pathlib import Path
from _parser import extract_resources
from _aws_helpers import init_aws_clients, aws_create_resource
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

    # AWS
    boto_clients = init_aws_clients()
    created = {k:0 for k in ('sqs','sns','s3','lambda','k8s')}
    for svc in ('sqs','sns','s3','lambda'):
        for it in resources.get(svc, []):
            if isinstance(it, str) and it.startswith('arn:aws:'):
                it = it.split(':')[-1]
            if aws_create_resource(boto_clients, svc, it):
                created[svc] += 1

    # K8s
    if resources.get('k8s'):
        print("🧩 Handling K8s...")
        created['k8s'] = create_k8s_from_struct(resources['k8s']) if isinstance(resources['k8s'], dict) else 0

    # Summary
    print("\n🎉 Setup summary:")
    for k, v in created.items():
        print(f" - {k.upper():12}: {v}")
    print(f"\nElapsed: {time.time()-start:.1f}s")

if __name__ == "__main__":
    import sys
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    run_setup(arg)
