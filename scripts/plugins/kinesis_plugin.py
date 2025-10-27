# scripts/plugins/kinesis_plugin.py
from .base_plugin import AWSResourcePlugin
import logging

logger = logging.getLogger(__name__)

class KinesisPlugin(AWSResourcePlugin):
    def __init__(self):
        super().__init__('kinesis')

    def validate_name(self, name: str) -> bool:
        # Names: 1–128 alphanumeric + underscores + hyphens
        import re
        return bool(name and re.match(r'^[a-zA-Z0-9_-]{1,128}$', name))

    def resource_exists(self, client, name: str) -> bool:
        try:
            streams = client.list_streams(Limit=100)
            return name in streams.get('StreamNames', [])
        except Exception:
            return False

    def create_resource(self, client, name: str, context: dict = None):
        try:
            client.create_stream(StreamName=name, ShardCount=1)
            logger.info(f"Kinesis stream created: {name}")
            return {'status': 'created', 'stream_name': name}
        except Exception as e:
            raise Exception(f"Failed to create Kinesis stream {name}: {e}")
