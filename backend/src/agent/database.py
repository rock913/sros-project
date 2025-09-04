import os
import uuid
from sqlalchemy import create_engine, Column, Text, String
from sqlalchemy.dialects.postgresql import UUID
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
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(1024))

def get_db_connection():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def init_db():
    with engine.connect() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        connection.commit()
    Base.metadata.create_all(bind=engine)

def insert_documents(documents: list):
    db = SessionLocal()
    try:
        for doc_data in documents:
            doc_obj = Document(content=doc_data["text"], embedding=doc_data["embedding"])
            db.add(doc_obj)
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
