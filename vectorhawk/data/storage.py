from elasticsearch import Elasticsearch, exceptions
from vectorhawk.core.config import Config
import logging

logger = logging.getLogger("vectorhawk")


class ElasticsearchHandler:
    def __init__(self):
        self.es = Elasticsearch(
            [Config.ELASTICSEARCH_HOST],
            http_auth=(Config.ELASTICSEARCH_USER, Config.ELASTICSEARCH_PASSWORD),
            timeout=30,
        )

    def index_document(self, index_name, document, doc_id=None):
        try:
            response = self.es.index(index=index_name, id=doc_id, body=document)
            logger.info(f"Document indexed with ID: {response['_id']}")
            return response
        except exceptions.ElasticsearchException as e:
            logger.error(f"Error indexing document: {e}")
            raise

    def search_documents(self, index_name, query):
        try:
            response = self.es.search(index=index_name, body={"query": query})
            return response["hits"]["hits"]
        except exceptions.ElasticsearchException as e:
            logger.error(f"Error searching documents: {e}")
            raise
