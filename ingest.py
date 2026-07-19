''' 
load_pdf_text -> extract pdf and join return text and pages
'''

import sys 
import chromadb
import ollama 
from pypdf import PdfReader
import config

def load_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    pages_text  = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages_text), len(pages_text)

def chunk_text(text, chunk_size, chunk_overlap):
    chunks = []
    start = 0 
    while start <len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start  =  end - chunk_overlap
        if start <= 0:
            break

    return [c.strip() for c in chunks if c.strip()]

def embed_text(text):
    response = ollama.embeddings(model = config.EMBEDDING_MODEL, prompt = text)
    return response["embedding"]


def main():
    if len(sys.argv) < 2:
        print("Please provide path, Usage: python ingest.py path/to/document.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]
    full_text, num_pages  = load_pdf_text(pdf_path)

    if not full_text:
        print("Empty pdf or unable to extract")
        sys.exit(1)


    chunks = chunk_text(full_text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)

    client = chromadb.PersistentClient(path = config.VECTOR_DB)
    collection = client.get_or_create_collection(name = config.COLLECTION_NAME)

    for i, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        collection.add(ids=[f"{pdf_path}-{i}"], 
                        embedding = [embedding], 
                        documents = [chunk],
                        metadatas = [{"source": pdf_path, "chunk_index": i}])
    print("Done with embedding and storing")
    print(f"Collection has {collection.count()} chunks")




if __name__ == "__main__":
    main()
