import chromadb
from chromadb.config import Settings
from app.config import (
    CHROMA_DB_DIR, COLLECTION_NAME
)
# ---------- ChromaDB ----------
_CHROMA_SETTINGS = Settings(anonymized_telemetry=False)

def get_collection():
    """Get the existing ChromaDB collection."""
    client = chromadb.PersistentClient(
        path=CHROMA_DB_DIR,
        settings=_CHROMA_SETTINGS
    )

    return client.get_or_create_collection(
        name=COLLECTION_NAME
    )