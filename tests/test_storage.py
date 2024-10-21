import pytest
from vectorhawk.data.storage import ElasticsearchHandler


@pytest.fixture(scope="module")
def es_handler():
    handler = ElasticsearchHandler()
    test_index = "test_index"
    test_document = {
        "title": "Test Document",
        "content": "This is a test document for Elasticsearch.",
    }

    # Create the index before running tests
    handler.es.indices.create(
        index=test_index, ignore=400
    )  # Ignore if index already exists
    yield handler
    handler.es.indices.delete(
        index=test_index, ignore=[400, 404]
    )  # Cleanup after tests


def test_index_document(es_handler):
    response = es_handler.index_document(
        "test_index",
        {
            "title": "Test Document",
            "content": "This is a test document for Elasticsearch.",
        },
    )
    assert response is not None
    assert "_id" in response


def test_search_documents(es_handler):
    # Index a document first
    es_handler.index_document(
        "test_index",
        {
            "title": "Test Document",
            "content": "This is a test document for Elasticsearch.",
        },
    )
    query = {"match": {"title": "Test Document"}}
    results = es_handler.search_documents("test_index", query)
    assert len(results) > 0
