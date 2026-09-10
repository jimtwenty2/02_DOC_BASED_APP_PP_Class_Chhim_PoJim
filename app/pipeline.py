from app.retriever import retrieve
from app.generator import generate_answer


def user_query(query: str) -> str:

    # Retrieve relevant chunks
    chunks = retrieve(query)

    #  Generate answer from retrieved chunks
    answer = generate_answer(query, chunks)

    return answer