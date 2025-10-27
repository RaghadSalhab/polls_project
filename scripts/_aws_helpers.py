# scripts/_aws_helpers.py 
import time
import logging
from plugins.sqs_plugin import SQSPlugin
from plugins.sns_plugin import SNSPlugin
from plugins.s3_plugin import S3Plugin
from plugins.kinesis_plugin import KinesisPlugin

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class PluginManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.plugins = {
                'sqs': SQSPlugin(),
                'sns': SNSPlugin(),
                's3': S3Plugin(),
                'kinesis': KinesisPlugin(), 

            }
        return cls._instance

    def get_plugin(self, service: str):
        return self.plugins.get(service)


def init_aws_clients(endpoint="http://localhost:4566"):
    try:
        import boto3
        session = boto3.Session(
            aws_access_key_id="test",
            aws_secret_access_key="test",
            region_name="us-east-1"
        )

        clients = {}
        for service in ['sqs','sns','s3','lambda','kinesis']:
            try:
                clients[service] = session.client(service, endpoint_url=endpoint)
                logger.info(f"Initialized {service} client")
            except Exception as e:
                logger.warning(f"Skipping {service}: {e}")

        return clients
    except ImportError:
        logger.error("boto3 not installed")
        return None


def aws_create_resource(clients, service: str, name: str, max_retries: int = 3):
    if clients is None or service not in clients:
        logger.error(f"No client available for {service}")
        return False

    plugin_manager = PluginManager()
    plugin = plugin_manager.get_plugin(service)
    if not plugin:
        logger.error(f"No plugin found for service: {service}")
        return False

    if not plugin.validate_name(name):
        logger.error(f"Invalid {service} name: {name}")
        return False

    if plugin.resource_exists(clients[service], name):
        logger.info(f"{service.upper()} exists: {name}")
        return True

    for attempt in range(max_retries):
        try:
            plugin.create_resource(clients[service], name)
            logger.info(f"Created {service.upper()}: {name}")
            return True
        except Exception as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed to create {service} '{name}': {e}")
                return False
            else:
                logger.warning(f"Retry {attempt+1}/{max_retries} for {service} '{name}'")
                time.sleep(1)

    return False
