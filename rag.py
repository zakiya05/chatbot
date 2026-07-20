import ollama 
import chromadb
import config

_client = chromadb.PersistentClient(path=config.VECTOR_DB_DIR)
_collection = _client.get_or_create_collection(name=config.COLLECTION_NAME)

def has_documents():
    return _collection.count() > 0

def retrieve_context(query):
    if _collection.count() == 0:
        return "" 
 
  
    query_embedding = ollama.embeddings(
        model=config.EMBEDDING_MODEL, prompt=query
    )["embedding"]
 
  
    results = _collection.query(
        query_embeddings=[query_embedding], n_results=config.TOP_K
    )
 
    chunks = results["documents"][0]
    return "\n\n".join(chunks)

def get_response(conversation_history, retrieved_context):
    system_prompt = config.SYSTEM_PROMPT
 
   
    if retrieved_context:
        system_prompt += (
            "\n\nUse the following context from the user's documents to "
            "help answer the question, if it's relevant. If the context "
            "doesn't contain the answer, just answer normally.\n\n"
            f"Context:\n{retrieved_context}"
        )
 
    messages = [{"role": "system", "content": system_prompt}] + conversation_history
    response = ollama.chat(model=config.MODEL, messages=messages)
    return response["message"]["content"]