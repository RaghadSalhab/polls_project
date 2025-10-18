from elasticsearch import Elasticsearch

class ElasticClient:
    _instance = None

    @classmethod
    def get_client(cls):
        if cls._instance is None:
            # cls._instance = Elasticsearch(
            #     "http://localhost:9200",
            #     basic_auth=("elastic", "drpwnuVhPq*T_kFHjJp5")
            # )
            cls._instance = Elasticsearch(
                "http://host.docker.internal:9200",
                basic_auth=("elastic", "drpwnuVhPq*T_kFHjJp5")
                    )

        return cls._instance
