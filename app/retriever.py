from typing import List, TypedDict
from app.config import (TOP_K,MAX_DISTANCE)
from app.embedding import embed_query
from app.chromadb_config import get_collection

class RetrievedChunk(TypedDict):
    text: str
    source: str
    chunk_index: int
    distance: float

def retrieve(query: str, top_k: int = TOP_K):

    collection = get_collection()

    query_embeddings = embed_query(query)

    results = collection.query(
        query_embeddings = [query_embeddings],
        n_results = top_k,
        include = [
            "documents",
            "metadatas",
            "distances"
        ]
    )

    chunks: List[RetrievedChunk] = []
    
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for text, meta, distance in zip(documents,metadatas,distances):
        if distance <= MAX_DISTANCE:
            chunks.append(
                {
                    "text": text,
                    "source": meta.get("source","unknown"),
                    "chunk_index": meta.get("chunk_index",-1),
                    "distance": distance
                } #type:ignore
            )

    return chunks

    return chunks


def print_chunks(chunks: List[RetrievedChunk]) -> None:
    print(f"\nTOP_K Chunk : [{len(chunks)}]")
    print("=" * 80)
    print(f"{'source':<60} {'distance':>12} {'rank':>6}")
    for i, chunk in enumerate(chunks, start=1):
        print(f"{chunk['source']:<60} {chunk['distance']:>12.4f} {i:>6}")
    print()