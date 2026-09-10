from app.embedding import embed_query
from app.chromadb_config import get_collection

TEST_QUERY = "How to backup file?"
TOP_K = 3


def main():
    # Embed the test question
    query_embedding = embed_query(TEST_QUERY)

    #  Connect to ChromaDB
    collection = get_collection()

    # Search for the top 3 most similar chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K,
    )

    print("\n========== VECTOR STORE CHECK ==========")
    print(f"Query: {TEST_QUERY}\n")

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    if not documents:
        print("No results found.")
        return

    for i, (document, metadata, distance) in enumerate(
        zip(documents, metadatas, distances),
        start=1,
    ):
        source = (
            metadata.get("source", "Unknown")
            if metadata
            else "Unknown"
        )

        preview = document[:200].replace("\n", " ")

        print(f"[{i}] Source: {source}")
        print(f"    Distance: {distance:.4f}")
        print(f"    Text: {preview}...")
        print()

    print("========================================")


if __name__ == "__main__":
    main()