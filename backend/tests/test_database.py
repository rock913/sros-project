import pytest
import os
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text
from agent.database import get_db_connection, init_db, upsert_documents, query_documents, Document, Base

# Use a fixture to manage the PostgreSQL test container
@pytest.fixture(scope="module")
def postgres_container():
    with PostgresContainer("postgres:16-alpine") as postgres:
        os.environ["DATABASE_URL"] = postgres.get_connection_url()
        yield postgres
    del os.environ["DATABASE_URL"]

@pytest.fixture(scope="function")
def db_session(postgres_container):
    # Initialize the database schema for each test function
    init_db()
    # Get a new connection for the test
    session = get_db_connection()
    yield session
    # Clean up the database after each test
    session.close()
    engine = create_engine(os.environ["DATABASE_URL"])
    with engine.connect() as connection:
        # Drop all tables defined in Base.metadata
        Base.metadata.drop_all(bind=engine)
        connection.commit()

def test_init_db(db_session):
    # Check if the documents table exists
    result = db_session.execute(
        text("SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename  = 'documents');")
    ).scalar()
    assert result is True

    # Check if the pgvector extension is enabled
    result = db_session.execute(
        text("SELECT EXISTS (SELECT FROM pg_extension WHERE extname = 'vector');")
    ).scalar()
    assert result is True

def test_upsert_and_query_documents(db_session):
    # Test upserting documents
    doc1 = {"id": "doc1", "text": "This is a test document about AI.", "embedding": [0.1]*1024}
    doc2 = {"id": "doc2", "text": "Another document on machine learning.", "embedding": [0.4]*1024}
    
    upsert_documents([doc1, doc2])

    # Test querying documents
    query_embedding = [0.1]*1024
    results = query_documents(query_embedding, k=1)
    
    assert len(results) == 1
    assert results[0].id == "doc1"
    assert results[0].content == "This is a test document about AI."

    # Test upserting an existing document (update)
    doc1_updated = {"id": "doc1", "text": "Updated test document about AI.", "embedding": [0.7]*1024}
    upsert_documents([doc1_updated])

    results_updated = query_documents([0.7]*1024, k=1)
    assert len(results_updated) == 1
    assert results_updated[0].id == "doc1"
    assert results_updated[0].content == "Updated test document about AI."
    assert results_updated[0].embedding == [0.7]*1024

def test_query_documents_no_results(db_session):
    query_embedding = [0.9]*1024
    results = query_documents(query_embedding, k=1)
    assert len(results) == 0

def test_query_documents_multiple_results(db_session):
    doc1 = {"id": "doc1", "text": "Apple is a fruit.", "embedding": [0.1]*1024}
    doc2 = {"id": "doc2", "text": "Orange is a fruit.", "embedding": [0.15]*1024}
    doc3 = {"id": "doc3", "text": "Banana is a fruit.", "embedding": [0.2]*1024}
    
    upsert_documents([doc1, doc2, doc3])

    query_embedding = [0.1]*1024
    results = query_documents(query_embedding, k=3)
    
    assert len(results) == 3
    assert results[0].id == "doc1"
    assert results[1].id == "doc2"
    assert results[2].id == "doc3"