import os 
from typing import List, Tuple
import chromadb 
from chromadb.config import Settings

from app.config import (
    CHROMA_DB_DIR,
    DATA_DIR,
    CHUNK_SIZE, CHUNK_OVERLAP,
    COLLECTION_NAME
)

from app.embedding import embed_texts

def _read_text(path: str) -> str:
    with open(path, 'r', encoding='UTF-8') as file:
        return file.read()

# Load specific amount of document in /{DATA_DIR} and extract text from each document
def load_document(count_file: int, data_dir: str = DATA_DIR) -> List[Tuple[str, str]]:
    documents = []
    list_docs = os.listdir(data_dir)
    for filename in sorted(list_docs):

        # count_file use to count how many file we want to load and extract text
        count_file += 1

        if count_file <= len(list_docs):
            path = os.path.join(data_dir, filename)
            if not os.path.isfile(path):
                continue
            ext = filename.lower().rsplit(".",1)[-1]
            if ext == "txt":
                text = _read_text(path)
            else:
                continue

        if text.strip():
            documents.append((filename,text))

    return documents

# ---------- Chunking ----------
def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP
) -> List[str]:
    """ FIxed size strategy with overlapping"""
    text = text.strip()
    if not text:
        return []
    chunks = []
    chunk_count = 0;
    start = 0
    while start < len(text):
        chunk_count += 1
        end = start + chunk_size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - chunk_overlap

    return chunks

# ---------- Indexing ----------
_CHROMA_SETTINGS = Settings(anonymized_telemetry=False)

def get_collection():

    # Store the Chroma database persistently on disk
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR, settings=_CHROMA_SETTINGS)
    try:
        # Try to delete if exist and rebuild new one
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    # Return the collection or create it if it does not exist
    return client.get_or_create_collection(name=COLLECTION_NAME)

def build_index(count_file: int ,data_dir: str = DATA_DIR) -> int:

    collection = get_collection()

    docments = load_document(count_file,data_dir)

    if not docments:
        raise FileNotFoundError(f"No file .txt or .md was found")

    ids, texts, metadatas = [], [], []

    for filename, full_text, in docments:
        for i, chunk in enumerate(chunk_text(full_text)):
            ids.append(f"{filename}::{i}")
            texts.append(chunk)
            metadatas.append({
                "source": filename,
                "chunk_index":i
            })
    embeddings = embed_texts(texts)
    collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
    )

    return len(texts)