import pytest
import os
from sqlalchemy import create_engine, text
from agent.database import get_db_connection, init_db, insert_documents, query_documents, Document, Base, SessionLocal
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use a fixture to manage the database setup and teardown for the entire module
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Check if the DATABASE_URL is set
    database_url = os.getenv("POSTGRES_URI")
    if not database_url:
        pytest.fail("POSTGRES_URI environment variable not set. Please create a .env file with the variable.")

    # Initialize the database schema once for the module
    init_db()
    yield
    # Clean up the database after all tests in the module have run
    engine = create_engine(database_url)
    with engine.connect() as connection:
        # Drop all tables defined in Base.metadata
        Base.metadata.drop_all(bind=engine)
        connection.commit()

@pytest.fixture(scope="function")
def db_session():
    # Get a new connection for the test
    session = SessionLocal()
    yield session
    # Clean up the database after each test
    session.query(Document).delete()
    session.commit()
    session.close()

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

def test_simple_insert_and_query(db_session):
    doc1 = {"text": "This is a test document about AI.", "embedding": [0.1]*1024}
    doc2 = {"text": "Another document on machine learning.", "embedding": [0.4]*1024}
    
    insert_documents([doc1, doc2])

    query_embedding = [0.1]*1024
    results = query_documents(query_embedding, k=1)
    
    assert len(results) == 1
    assert results[0].content == "This is a test document about AI."

def test_query_documents_no_results(db_session):
    query_embedding = [0.9]*1024
    results = query_documents(query_embedding, k=1)
    assert len(results) == 0

def test_query_documents_multiple_results(db_session):
    doc1 = {"text": "Apple is a fruit.", "embedding": [0.1]*1024}
    doc2 = {"text": "Orange is a fruit.", "embedding": [0.15]*1024}
    doc3 = {"text": "Banana is a fruit.", "embedding": [0.2]*1024}
    
    insert_documents([doc1, doc2, doc3])

    query_embedding = [0.1]*1024
    results = query_documents(query_embedding, k=3)
    
    assert len(results) == 3
    # The order is not guaranteed, so we check if the contents are correct
    result_contents = {r.content for r in results}
    assert result_contents == {"Apple is a fruit.", "Orange is a fruit.", "Banana is a fruit."}
