# scripts/plugins/s3_plugin.py 
from .base_plugin import AWSResourcePlugin
import botocore

class S3Plugin(AWSResourcePlugin):
    def __init__(self):
        super().__init__('s3')
    
    def create_resource(self, client, name: str, context: dict = None):
        try:
            client.create_bucket(Bucket=name)
            # Enable versioning for backup/archive buckets
            if any(x in name.lower() for x in ('backup', 'archive')):
                client.put_bucket_versioning(
                    Bucket=name,
                    VersioningConfiguration={'Status': 'Enabled'}
                )
            return {'status': 'created', 'bucket_name': name}
        except botocore.exceptions.ClientError as e:
            raise RuntimeError(f"S3 create_bucket failed for {name}: {e}")
    
    def resource_exists(self, client, name: str) -> bool:
        try:
            response = client.list_buckets()
            return any(bucket['Name'] == name for bucket in response.get('Buckets', []))
        except botocore.exceptions.ClientError:
            return False
    
    def get_smart_attributes(self, name: str) -> dict:
        attrs = {}
        if 'backup' in name.lower() or 'archive' in name.lower():
            attrs['Versioning'] = 'Enabled'
        return attrs
