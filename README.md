# Embedding Storage with ChromaDB 

This project reads texts from a file, generates embeddings using the AI21 API, and stores them in a ChromaDB collection.

## Requirements

- Python 3.6+
- `requests` library
- `chromadb` library

## Setup

1. Clone the repository and navigate to it:
    ```bash
    git clone https://github.com/yourusername/embedding-storage.git
    cd embedding-storage
    ```

2. Install the required packages:
    ```bash
    pip install requests chromadb
    ```

3. Set your AI21 API key in `main.py`:
    ```python
    ai21_api_key = "YOUR_API_KEY_HERE"
    ```

## Usage

1. Prepare a text file with one text entry per line.
2. Run the script:
    ```bash
    python main.py
    ```
3. Enter the filename when prompted.

## Code Overview

- `get_ai21_embeddings(texts, embed_type="segment")`: Generates embeddings using the AI21 API.
- `store_embeddings_with_ids(embeddings, texts)`: Stores embeddings in ChromaDB.
- `generate_and_store_embeddings_with_ids(texts)`: Orchestrates embedding generation and storage.
- `read_texts_from_file(filename)`: Reads texts from a file.
- `if __name__ == "__main__"`: Main entry point of the script.


