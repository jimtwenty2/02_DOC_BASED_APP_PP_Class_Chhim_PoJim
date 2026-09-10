from typing import List, TypedDict
from app.config import TOP_K
from app.embedding import embed_query
from app.ingest import get_collection

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
        chunks.append(
            {
                "text": text,
                "source": meta.get("source","unknown"),
                "chunk_index": meta.get("chunk_index",-1),
                "distance": distance
            } #type:ignore
        )

    return chunks