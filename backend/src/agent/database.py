import os
from sqlalchemy import create_engine, Column, Integer, Text, String
from sqlalchemy.orm import sessionmaker, declarative_base
from pgvector.sqlalchemy import Vector
from dotenv import load_dotenv
from sqlalchemy import text

load_dotenv()

DATABASE_URL = os.getenv("POSTGRES_URI")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, index=True) # Changed to String for custom IDs
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1024)) # Assuming Gemini embedding size of 1024

def get_db_connection():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    with engine.connect() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        connection.commit()

def upsert_documents(documents: list):
    db = SessionLocal()
    try:
        for doc_data in documents:
            # Check if document with this ID already exists
            existing_doc = db.query(Document).filter(Document.id == doc_data["id"]).first()
            if existing_doc:
                # Update existing document
                existing_doc.content = doc_data["text"]
                existing_doc.embedding = doc_data["embedding"]
            else:
                # Create new document
                new_doc = Document(id=doc_data["id"], content=doc_data["text"], embedding=doc_data["embedding"])
                db.add(new_doc)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def query_documents(query_embedding: list, k: int = 5):
    db = SessionLocal()
    try:
        results = db.query(Document).order_by(Document.embedding.cosine_distance(query_embedding)).limit(k).all()
        return results
    finally:
        db.close()
