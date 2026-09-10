# Document Based Application - RAG Implementation

## 1. Installation
Clone the repository and enter the project directory:

```
git clone https://github.com/jimtwenty2/02_DOC_BASED_APP_PP_Class_Chhim_PoJim.git
cd 02_DOC_BASED_APP_PP_Class_Chhim_PoJim
```

Install all dependencies from pyproject.toml and poetry.lock:

```poetry install```


Get the virtual-environment activation command:

```poetry env activate```

Copy and execute the command displayed by Poetry to activate virtual environment. For example:

```source /path/to/poetry/virtualenv/bin/.../activate```

## 2. Prepare Documents

Put your .txt documents inside a directory.

For example: inside `documents/`

The directory can also be another location. You will be able to enter the directory when running the vector store.

## 3. Build the Vector Store
The first step is to load the documents, split them into chunks, generate embeddings, and store everything in ChromaDB.

From the root project directory, run:

```poetry run python -m app.vector_store```

You will be asked:

========== RAG Index Builder ==========
- Enter number of files to load:
- Enter document folder [default: ...]:

### Important Note About Number of Files

The number of files you enter does not need to exactly match the number of files in the directory.

For example, if the directory contains: 5 files

and you enter:

`Enter number of files to load: 10`

the program will simply load all available files.

So:

- Available files: 5
- Requested files: 10
- Result: 5 files loaded

You can enter any positive number. If the requested number is greater than the number of available files, the program loads all available files instead of producing an error.

## 4. Verify the Vector Store

Before running the chatbot, verify that the vector search is working correctly.

Run:

```poetry run python -m app.demo_vector_check```

The script will:

- Take a test question
- Convert the question into an embedding
- Search ChromaDB
- Return the top 3 most similar chunks

Check whether the returned chunks are relevant to your question.
If the results make sense, the vector store and retrieval process are working correctly.

## 5. Run the RAG Chatbot
After the vector store has been built and verified, run the chatbot from the project root:

```poetry run python -m app.main```
