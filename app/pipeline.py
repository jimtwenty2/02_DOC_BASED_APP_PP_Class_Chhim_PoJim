from app.retriever import (retrieve, print_chunks)
from app.generator import generate_answer


def user_query(query: str) -> str:

    # Retrieve relevant chunks
    chunks = retrieve(query)
    print_chunks(chunks)

    #  Generate answer from retrieved chunks
    answer = generate_answer(query, chunks)

    return answer