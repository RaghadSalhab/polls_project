# scripts/plugins/base_plugin.py
from abc import ABC, abstractmethod
import re

class AWSResourcePlugin(ABC):
    def __init__(self, service_name: str):
        self.service_name = service_name
    
    def validate_name(self, name: str) -> bool:
        if not name or not isinstance(name, str):
            return False
            
        rules = {
            's3': (3, 63, r'^[a-z0-9.-]+$'),
            'sqs': (1, 80, r'^[a-zA-Z0-9_-]+$'),
            'sns': (1, 256, r'^[a-zA-Z0-9_-]+$'),
        }
        
        if self.service_name in rules:
            min_len, max_len, pattern = rules[self.service_name]
            if len(name) < min_len or len(name) > max_len:
                return False
            if not re.match(pattern, name):
                return False
        
        return True
    
    @abstractmethod
    def create_resource(self, client, name: str, context: dict = None):
        pass
    
    @abstractmethod  
    def resource_exists(self, client, name: str) -> bool:
        pass
    
    def get_smart_attributes(self, name: str) -> dict:
        return {}