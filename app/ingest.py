import os 
from typing import List, Tuple
import chromadb 
from chromadb.config import Settings

from app.config import (
    CHROMA_DB_DIR,
    DATA_DIR,
    CHUNK_SIZE, CHUNK_OVERLAP,
    COLLECTION_NAME,
    FILE_TO_LOAD
)

from app.embedding import embed_texts

def _read_text(path: str) -> str:
    # Read the entire text file using UTF-8 encoding
    with open(path, 'r', encoding='UTF-8') as file:
        return file.read()

# Load up to the requested number of .txt documents
def load_document(
    count_file: int = FILE_TO_LOAD,
    data_dir: str = DATA_DIR
) -> List[Tuple[str, str]]:

    documents = []
    count = 0

    # Loop through all files in the data directory in sorted order
    for filename in sorted(os.listdir(data_dir)):

       # Stop when the requested file count is reached
        if count >= count_file:
            break

        path = os.path.join(data_dir, filename)

         # Skip directories and non-file items
        if not os.path.isfile(path):
            continue

        # Extract file's extension
        ext = filename.lower().rsplit(".", 1)[-1]

        # Only process .txt files
        if ext != "txt":
            continue

        text = _read_text(path)

        # Skip empty files
        if not text.strip():
            continue

        documents.append((filename, text))
        count += 1

    return documents

# ---------- Chunking ----------
def chunk_text(
    text: str,
    chunk_size: int = CHUNK_SIZE,
    chunk_overlap: int = CHUNK_OVERLAP
) -> List[str]:
    
    """Split text into fixed-size overlapping chunks."""

    text = text.strip()

    if not text:
        return []

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])

        # Stop when the end of the document is reached
        if end >= len(text):
            break

        # Move back by the overlap amount for the next chunk
        start = end - chunk_overlap

    return chunks

# ---------- Indexing ----------
_CHROMA_SETTINGS = Settings(anonymized_telemetry=False)

def get_collection():

    # Create a persistent ChromaDB client
    client = chromadb.PersistentClient(path=CHROMA_DB_DIR, settings=_CHROMA_SETTINGS)

    try:
        # Delete the old collection to rebuild the index from scratch
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    # Create a new collection for storing document embeddings
    return client.create_collection(name=COLLECTION_NAME)

# -------- Store embedded vector --------
def build_index(count_file: int ,data_dir: str = DATA_DIR) -> dict:

    # Create a fresh ChromaDB collection
    collection = get_collection()

    # Load documents and extract their text
    documents = load_document(count_file,data_dir)

    if not documents:
        raise FileNotFoundError(f"No file .txt was found")

    ids, texts, metadatas = [], [], []
    files_chunks = {}

    for filename, full_text in documents:

        chunked_text = chunk_text(full_text)

        files_chunks[filename] = len(chunked_text)

        for i, chunk in enumerate(chunked_text):
            ids.append(f"{filename}::{i}")
            texts.append(chunk)
            metadatas.append({
                "source": filename,
                "chunk_index":i
            })

    # Convert text chunks into vector embeddings
    embeddings = embed_texts(texts)

    # Store chunks, embeddings, and metadata in ChromaDB
    collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
    )

    return {
        "files_chunks": files_chunks,
        "chunks": len(texts),
        "status": "Indexing completed"
    }

if __name__ == '__main__':

    # Load documents, create embeddings, and store them in ChromaDB
    built_index = build_index(102)

    print("\n------------------------------ Result ------------------------------")
    print(f"Status: {built_index['status']}")
    print(f"Total Chunks Indexed: {built_index['chunks']} chunks")

    files_chunks = built_index["files_chunks"]
    print("------------------------------ Files -------------------------------")
    print(f"Total Files: {len(files_chunks)}")
    for filename, chunk_count in files_chunks.items():
        print(f"   {filename} ==> {chunk_count} chunks")
    print()