import pytest
from vectorhawk.data.storage import ElasticsearchHandler

@pytest.fixture
def es_handler():
    # No need to pass parameters manually; ElasticsearchHandler will use Config.
    return ElasticsearchHandler()

def test_index_document(es_handler):
    # Clean up the index first if it exists
    es_handler.es.options(ignore_status=[400, 404]).indices.delete(index="test_index")

    # Create the index
    es_handler.es.options(ignore_status=[400]).indices.create(index="test_index")

    # Index a document
    response = es_handler.index_document(
        "test_index",
        {
            "title": "Test Document",
            "content": "This is a test document for Elasticsearch.",
        },
    )
    assert response is not None

def test_search_documents(es_handler):
    # Index a document first
    es_handler.index_document(
        "test_index",
        {
            "title": "Test Document",
            "content": "This is a test document for Elasticsearch.",
        },
    )

    # Refresh the index
    es_handler.es.indices.refresh(index="test_index")

    query = {"match": {"title": "Test Document"}}
    results = es_handler.search_documents("test_index", query)
    assert len(results) > 0
