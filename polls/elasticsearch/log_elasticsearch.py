from .elastic_client import ElasticClient
from datetime import datetime

class LogElasticsearch:
    INDEX = "poll_logs"

    def __init__(self):
        self.es = ElasticClient.get_client()

    def log_event(self, level, message, user_id=None, endpoint=None, action=None, object_type=None, object_id=None, details=None):
        doc = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            "user_id": user_id,
            "endpoint": endpoint,
            "action": action,
            "object_type": object_type,
            "object_id": object_id,
            "details": details
        }
        self.es.index(index=self.INDEX, document=doc)


    def search_logs(self, keyword=None, level=None):
        query = {"bool": {"must": []}}
        
        if keyword:
            query["bool"]["must"].append({
                "multi_match": {
                    "query": keyword,
                    "fields": ["message", "endpoint"]
                }
            })
        if level:
            query["bool"]["must"].append({"match": {"level": level}})
        
        result = self.es.search(index=self.INDEX, query=query, size=100)
        return [hit["_source"] for hit in result["hits"]["hits"]]
