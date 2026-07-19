import sys 
import chromadb
import ollama
import config

def main():
    if len(sys.argv)<2:
        print('please follow the format command: python test_search.py "your question here" ')
        sys.exit(1)

    query = sys.argv[1]
    client = chromadb.PersistantClient(path = config.VECTOR_DB)
    collection = client.get_or_create(name  = config.COLLECTION_NAME)
    if collection.count == 0:
        print("Empty vector db, please run the ingest first")
        sys.exit(1)
    query_embedding = ollama.embeddings(model= config.EMBEDDING_MODEL, prompt=query)["embedding"]
    results = collection.query(query_embedding= [query_embedding], n_results = 3)
    for i, (doc, distance) in enumerate(
        zip(results["documents"][0], results["distances"][0])
    ):
        print(f"Match {i + 1} (distance: {distance:.4f}) ---")
       
        print(doc[:300] + ("..." if len(doc) > 300 else ""))
        print()


    

if __name__ == "__main__":
    main()