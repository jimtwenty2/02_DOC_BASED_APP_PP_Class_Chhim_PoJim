import os 
from typing import List, Tuple

from app.config import (
    DATA_DIR,
    CHUNK_SIZE, CHUNK_OVERLAP,
    FILE_TO_LOAD
)

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