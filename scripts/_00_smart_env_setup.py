# scripts/_00_smart_env_setup.py

import time
import os
import sys
from pathlib import Path
import logging

from _parser import extract_resources
from _aws_helpers import init_aws_clients, aws_create_resource, PluginManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

DJANGO_SETTINGS_PATH = os.environ.get(
    "DJANGO_SETTINGS_MODULE",
    "/app/my_poll_project/settings/dev.py"
)

def run_setup(settings_path=None):
    start_time = time.time()
    settings_path = settings_path or DJANGO_SETTINGS_PATH

    if not Path(settings_path).exists():
        logger.error(f"Settings not found at {settings_path}")
        return

    logger.info(f"Scanning settings: {settings_path}")
    resources = extract_resources(settings_path)

    # Initialize AWS clients
    logger.info("Initializing AWS clients...")
    boto_clients = init_aws_clients()
    if boto_clients is None:
        logger.error("Failed to initialize AWS clients")
        return

    # Track created resources
    created_count = {k: 0 for k in ('sqs', 'sns', 's3', 'lambda', 'dynamodb', 'events', 'kinesis')}

    # Process each AWS service (added kinesis)
    for service in ('sqs', 'sns', 's3', 'lambda', 'dynamodb', 'events', 'kinesis'):
        resource_list = resources.get(service, [])
        if resource_list:
            logger.info(f"Processing {service.upper()} resources...")
            for resource_name in resource_list:
                # Extract name if it's an ARN
                if isinstance(resource_name, str) and resource_name.startswith('arn:aws:'):
                    resource_name = resource_name.split(':')[-1]

                if aws_create_resource(boto_clients, service, resource_name):
                    created_count[service] += 1

    # Summary
    logger.info("\nSetup Summary:")
    logger.info("=" * 40)
    total_created = sum(created_count.values())
    for svc, count in created_count.items():
        logger.info(f" - {svc.upper():12}: {count}")
    logger.info(f"\nTotal resources processed: {total_created}")
    logger.info(f"Elapsed time: {time.time() - start_time:.1f}s")


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    run_setup(arg)
