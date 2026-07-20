## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- [Ollama](https://ollama.com) installed and running

### Setup

Step 1: Install dependencies and pull the models
```
pip install -r requirements.txt
ollama pull tinyllama
ollama pull nomic-embed-text
```

Step 2: Ingest a document (do this before chatting, so answers are grounded in it)
```
python ingest.py path/to/your/document.pdf
```

Step 3 (optional): Sanity-check that retrieval works
```
python test_search.py "a question about the document"
```

Step 4: Chat
```
python3 chatbot.py
```

To exit the chat, type `quit` or `exit`.