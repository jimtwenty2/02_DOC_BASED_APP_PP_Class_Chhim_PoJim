from app.ingest import load_document, chunk_text_fixed_size
from app.embedding import embed_texts
from app.chromadb_config import get_collection
import os
from app.config import DATA_DIR

# ---------- Build and store vector index ----------
def build_index(count_file: int ,data_dir: str = DATA_DIR) -> dict:

    # Load documents and extract their text
    documents = load_document(count_file, data_dir)

    if not documents:
        raise FileNotFoundError(f"No file .txt was found in directory {data_dir}/")
    
    collection = get_collection()

    ids, texts, metadatas = [], [], []
    files_chunks = {}

    for filename, full_text in documents:

        chunked_text = chunk_text_fixed_size(full_text)

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

def main():
    print("==================== RAG Index Builder ====================")

    # Ask how many files to load
    while True:
        try:
            count_file = int(input("Enter number of files to load: ").strip())

            if count_file <= 0:
                print("Error: Number of files must be greater than 0.")
                continue
            break
        except ValueError:
            print("Error: Please enter a valid number.")

    # Ask for the folder containing the documents
    while True:
        data_dir = input(f"Enter document folder [default: {DATA_DIR}]: ").strip()

        # Use default folder if user presses Enter
        if not data_dir:
            data_dir = DATA_DIR

        # Check if folder exists
        if not os.path.exists(data_dir):
            print(f"Error: Folder does not exist: {data_dir}")
            continue

        # Check if path is a directory
        if not os.path.isdir(data_dir):
            print(f"Error: This path is not a folder: {data_dir}")
            continue

        break

    # ---------- Build index ----------
    try:
        result = build_index(
            count_file=count_file,
            data_dir=data_dir
        )

        print("\n==================== Indexing Result ====================")
        print(f"Status: {result['status']}")
        print(f"Total chunks: {result['chunks']}")

        print("\nFiles:")
        for filename, chunk_count in result["files_chunks"].items():
            print(f"  - {filename}: {chunk_count} chunks")

        print("=========================================================")

    except FileNotFoundError as e:
        print(f"\nError: {e}")

    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__": 
    main()