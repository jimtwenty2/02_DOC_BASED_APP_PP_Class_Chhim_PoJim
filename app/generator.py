from typing import List
import ollama

from app.config import GENERATE_MODEL, SYSTEM_PROMT
from app.retriever import RetrievedChunk

def build_prompt(query: str, chunks: List[RetrievedChunk]) -> str:
    """
        This is the 'prompt-augmentation' step before sending to LLM
        to Generate answer
    """

    if not chunks:
        context_block = "(No relevant chunk was found!)"
    else:
        context_block = "\n\n".join(
            f"[{i+1}] Source: {chunk['source']}\n{chunk['text']}"
            for i,chunk in enumerate(chunks)
        )
    return (
            f"Context:\n{context_block}\n\n"
            f"Query: {query}\n\n"
            "Answer using only the context above."
        )

def generate_answer(query: str, chunks: List[RetrievedChunk]) -> str:

    """ Generate an answer from the retrieved context using Ollama. """ 
    prompt = build_prompt(query, chunks) 
    
    response = ollama.chat(
        model=GENERATE_MODEL, 
        messages=[ 
            { "role": "system", "content": SYSTEM_PROMT},
            { "role": "user", "content": prompt },
        ], 
    ) 

    return response["message"]["content"].strip()