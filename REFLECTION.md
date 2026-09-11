# Reflection
For this RAG System, Here's my reflection for What worked well, What was harder than expected, Future improvement.

## What worked well
It's about overall RAG pipeline. The application can load documents, split into smaller chunks, generate embeddings, store them in Vector Store such ChromaDB, and retrieve relevant chunks when a user asks a question. and use a Ollama model allowed me to run the
embedding and generation steps in local.

## What was harder than expected
One thing that was harder than I expected was getting the retrieval results to
match the user's question accurately. but chunk size and content in that chunks can affect what info is retrived. In this case I use Fix-Sized splitting strategy, so if useful information is split into different chunks the retriever may not return the best context which cause LLM to generate not good answer. 

## Future improvement
For future improvement, I think we can use an Advanced RAG technique such as
re-ranking. right now system retrieves he top_k chunks direct from
VextorStore (chromadb) based on vector similarity. A re-ranking step can evaluate the
retrieved chunks again and place the most relevant chunks first before sending to LLM. This may improve retrieval accuracy and help the LLM generate more relevant and grounded answers.