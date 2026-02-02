import os
import uuid

from dotenv import load_dotenv
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, String, Text, create_engine, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("POSTGRES_URI")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(Text, nullable=False)
    # Underlying embedding column stored as pgvector.Vector
    # Use 2048 dimensions for embeddings to match Qwen3-Embedding-8B via SiliconFlow
    _embedding = Column("embedding", Vector(2048))
    source = Column(String, unique=True, index=True)  # Unique identifier for the document (e.g., DOI or URL)

    @property
    def embedding(self):
        """Return embedding as numpy array."""
        val = self._embedding
        if val is None:
            return None
        try:
            import numpy as _np

            return _np.array(val)
        except ImportError:
            return val

    @embedding.setter
    def embedding(self, value):
        """Accept numpy array or list, pad or truncate to correct dimensions, and store as list."""
        if value is None:
            self._embedding = None
            return
        # Convert numpy array to list for storage
        try:
            import numpy as _np
            vec = value.tolist() if isinstance(value, _np.ndarray) else list(value)
        except ImportError:
            vec = list(value)
        # Pad or truncate to match column dimension
        # Get target dimension from column type
        target_dim = Document.__table__.columns['embedding'].type.dim
        if len(vec) < target_dim:
            vec = vec + [0.0] * (target_dim - len(vec))
        elif len(vec) > target_dim:
            vec = vec[:target_dim]
        self._embedding = vec

def get_db_connection():
    """Return a live DB session (caller is responsible for closing).

    Previous implementation closed the session before the caller could use it,
    resulting in no persistence (queries returned empty). This fixes that bug.
    """
    return SessionLocal()

def init_db():
    with engine.connect() as connection:
        connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        connection.commit()
    Base.metadata.create_all(bind=engine)

def insert_documents(documents: list):
    db = SessionLocal()
    try:
        for doc_data in documents:
            doc_obj = Document(content=doc_data["text"], embedding=doc_data["embedding"], source=doc_data.get("source"))
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
        # Ensure query_embedding matches the expected vector dimension
        dim = Document.__table__.columns['embedding'].type.dim
        vec = list(query_embedding)
        if len(vec) < dim:
            vec = vec + [0.0] * (dim - len(vec))
        elif len(vec) > dim:
            vec = vec[:dim]
        # Use the underlying vector column for cosine distance
        results = (
            db.query(Document)
            .order_by(Document._embedding.cosine_distance(vec))
            .limit(k)
            .all()
        )
        return results
    finally:
        db.close()


def get_all_documents():
    db = SessionLocal()
    try:
        results = db.query(Document).all()
        return results
    finally:
        db.close()
