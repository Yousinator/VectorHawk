from elasticsearch import Elasticsearch
from ..core.config import Config  # Use Config
from ..core.exceptions import ElasticsearchError


class ElasticsearchHandler:
    def __init__(self):
        # Get configuration from Config class
        self.config = Config()
        es_host = self.config.ES_HOST
        es_username = self.config.ES_USER
        es_password = self.config.ES_PASSWORD

        # Initialize Elasticsearch client during object creation
        self.es = Elasticsearch(
            es_host,
            basic_auth=(es_username, es_password),
            request_timeout=30,
            max_retries=3,
            retry_on_timeout=True,
        )

    def index_document(self, index_name, document, doc_id=None):
        try:
            response = self.es.index(index=index_name, id=doc_id, body=document)
            return response
        except Exception as e:
            raise ElasticsearchError(f"Failed to index document: {e}")

    def search_documents(self, index_name, query):
        try:
            response = self.es.search(index=index_name, body={"query": query})
            return response["hits"]["hits"]
        except Exception as e:
            raise ElasticsearchError(f"Search failed: {e}")
