import ollama 
import config
import chromadb

_client = chromadb.PersistentClient(path=config.VECTOR_DB_DIR)
_collection = _client.get_or_create_collection(name=config.COLLECTION_NAME)

def retrieve_context(query):
    if _collection.count() ==0:
        print("no documents ingested")
        return ""
    query_embedding = ollama.embeddings(model= config.EMBEDDING_MODEL, prompt= query)['embedding']
    results = _collection.query(query_embeddings=[query_embedding],n_results=config.TOP_K)
    chunks = results["documents"][0]
    return "\n\n".join(chunks)


def get_response(conversation_history, retrieved_context):
    system_prompt = config.SYSTEM_PROMPT
    if retrieved_context:
        system_prompt+= (
            "\n\nUse the following context from the user's documents to "
            "help answer the question, if it's relevant. If the context "
            "doesn't contain the answer, just answer normally.\n\n"
            f"Context:\n{retrieved_context}"
        )
    
    messages = [{"role":"system", "content": system_prompt}] + conversation_history
    response = ollama.chat(model = config.MODEL, messages = messages)
    return response["message"]["content"]



def main():
    print(f"The model config is:{config.MODEL}")
    conversation_history = []
    while True:
        user_input = input("You:").strip()
        if user_input.lower() in ("quit", "exit"):
            print("Great chatting with you! Bye!")
            break
        if not user_input:
            continue
        conversation_history.append({"role": "user", "content": user_input})
        print("conversation history is: ", conversation_history)
        try:
            context = retrieve_context(user_input)
            reply = get_response(conversation_history, context)
        except Exception as e:
            print(f"Error calling local model: {e}")
            print("Check if Ollama is running? Try 'ollama serve' in another terminal.")
            conversation_history.pop()  
            continue
 
        conversation_history.append({"role": "assistant", "content": reply})
 
        print(f"Llama: {reply}\n")



if __name__ == "__main__":
     main()