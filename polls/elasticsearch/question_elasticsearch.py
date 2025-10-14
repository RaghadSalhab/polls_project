from .elastic_client import ElasticClient

class QuestionElasticsearch:
    INDEX = "questions"

    def __init__(self):
        self.es = ElasticClient.get_client()

    def index_question(self, question):
        self.es.index(
            index=self.INDEX,
            id=question.id,
            document={
                "question_text": question.question_text,
                "created_by_id": question.created_by_id,
                "pub_date": str(question.pub_date),
            }
        )

    def update_question(self, question_id, updated_data):
        self.es.update(
            index=self.INDEX,
            id=question_id,
            doc=updated_data
        )

    def delete_question(self, question_id):
        self.es.delete(index=self.INDEX, id=question_id, ignore=[404])

    def search_questions(self, keyword, page: int = 1, size: int = 10, fuzzy: bool = True):
        query_body = {
            "from": (page - 1) * size,
            "size": size,
            "query": {
                "multi_match": {
                    "query": keyword,
                    "fields": ["question_text"],
                    "fuzziness": "AUTO" if fuzzy else 0
                }
            },
            "highlight": {
                "fields": {"question_text": {}}
            }
        }

        result = self.es.search(index=self.INDEX, body=query_body)
        hits = []
        for hit in result["hits"]["hits"]:
            source = hit["_source"]
            if "highlight" in hit:
                source["highlight"] = hit["highlight"]
            hits.append(source)
        return hits
