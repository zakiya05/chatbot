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
    return []


def main():
    if len(sys.argv) < 2:
        print("Please provide path, Usage: python ingest.py path/to/document.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]
    full_text, num_pages  = load_pdf_text(pdf_path)

    if not full_text:
        print("Empty pdf or unable to extract")
        sys.exit(1)

    # chunking code 

    chunks = chunk_text(full_text, config.CHUNK_SIZE, config.CHUNK_OVERLAP)



if __name__ == "__main__":
    main()
