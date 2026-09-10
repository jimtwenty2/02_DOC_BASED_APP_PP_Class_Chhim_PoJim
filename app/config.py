# ---------- Models config ----------
EMBED_MODEL = 'nomic-embed-text:latest' 
GENERATE_MODEL = 'llama3.2:latest'

# ---------- Storage config ----------
DATA_DIR = str("documents")
CHROMA_DB_DIR = str("chroma_db")
COLLECTION_NAME = "documents"

# ----------Chuniking config ----------
CHUNK_SIZE = 600
CHUNK_OVERLAP = 120

# Default file number to load
FILE_TO_LOAD = 5

# ---------- Retrieval config ----------
TOP_K = 4
MAX_DISTANCE = 0.8 # Threshold

# ------ Generation config ------

# SYSTEM_PROMPT
SYSTEM_PROMT = (
    "You are helpful assistent that answers using ONLY the"
    "context provided below, if the answer is not contained in the context,"
    "say \"I could not find this in your documents.\""  # Grouded answer
    "Do not use any outside knowlegde. Cite the source file name(s) you used."
)
