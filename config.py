'''
Model and prompt to be configurable
'''
# Chat conversation
MODEL = "tinyllama:latest"

SYSTEM_PROMPT = "You are a helpful, concise assistant."

# Document Embedding dependencies

EMBEDDING_MODEL = "nomic-embed-text"
VECTOR_DB = "chroma_db"

COLLECTION_NAME = "documents_collection"

# Chunking parameters - change
CHUNK_SIZE = 500 
CHUNK_OVERLAP = 50