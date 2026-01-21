from typing import List, Optional

from agent.domain.ports.document_store import DocumentStore
from agent.database import Document as DbDocument, get_db_connection
from agent.domain.schemas.paper import Paper
