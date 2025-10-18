from .elastic_client import ElasticClient
from datetime import datetime
from polls.elasticsearch.log_elasticsearch import LogElasticsearch

class ChoiceElasticsearch:
    INDEX = "choices"

    log_es = LogElasticsearch() 

    def __init__(self):
        self.es = ElasticClient.get_client()

    def index_choice(self, choice):
        self.es.index(
            index=self.INDEX,
            id=choice.id,
            document={
                "choice_text": choice.choice_text,
                "question_id": choice.question_id,
                "votes": choice.votes
            }
        )
        self.log_es.log_event(
            level="INFO",
            action="CREATE",
            object_type="CHOICE",
            object_id=choice.id,
            message=f"Indexed new choice",
            details={"choice_text": choice.choice_text, "question_id": choice.question_id}
        )

    def update_choice(self, choice_id, updated_data):
        self.es.update(
            index=self.INDEX,
            id=choice_id,
            body={
                "doc": updated_data,
            }
        )
        self.log_es.log_event(
            level="INFO",
            action="UPDATE",
            object_type="CHOICE",
            object_id=choice_id,
            message=f"Updated choice",
            details=updated_data
        )


    def delete_choice(self, choice_id):
        self.es.delete(index=self.INDEX, id=choice_id, ignore=[404])
        self.log_es.log_event(
            level="INFO",
            action="DELETE",
            object_type="CHOICE",
            object_id=choice_id,
            message="Deleted choice"
        )

    def search_choices(self, keyword, page: int = 1, size: int = 10, fuzzy: bool = True):
        query_body = {
            "from": (page - 1) * size,
            "size": size,
            "query": {
                "multi_match": {
                    "query": keyword,
                    "fields": ["choice_text"],
                    "fuzziness": "AUTO" if fuzzy else 0
                }
            },
            "highlight": {
                "fields": {"choice_text": {}}
            }
        }

        result = self.es.search(index=self.INDEX, body=query_body)
        hits = []
        for hit in result["hits"]["hits"]:
            source = hit["_source"]
            if "highlight" in hit:
                source["highlight"] = hit["highlight"]
            hits.append(source)

        self.log_es.log_event(
            level="INFO",
            action="SEARCH",
            object_type="CHOICE",
            message=f"Searched choices with keyword '{keyword}'",
            details={"results_count": len(hits)}
        )

        return hits
