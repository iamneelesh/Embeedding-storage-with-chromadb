import requests
import chromadb
import uuid

# Chroma DB initialization
client = chromadb.PersistentClient(path="./chroma_db")
collection_name = "my_collection"

ai21_api_key = "your api key"
ai21_url = "https://api.ai21.com/studio/v1/embed"

def get_ai21_embeddings(texts, embed_type="segment"):
    headers = {
        "Authorization": f"Bearer {ai21_api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "texts": texts,
        "type": embed_type
    }

    try:
        response = requests.post(ai21_url, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()

        print("AI21 Response:", response_json)  # Debugging: Print AI21 response

        embeddings = []
        if "results" in response_json:
            for result in response_json["results"]:
                if "embedding" in result:
                    embeddings.append(result["embedding"])
                
        else:
            print(f"Unexpected AI21 response format: {response_json}")

        return embeddings

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error: {http_err}")
        print("Response Text:", response.text)
        return None
    except ValueError as value_err:
        print(f"ValueError: Failed to decode JSON response: {value_err}")
        print("Response Text:", response.text)
        return None
    except Exception as err:
        print(f"Other Error: {err}")
        return None

def store_embeddings_with_ids(embeddings, texts):
    try:
        collections = client.list_collections()
        collection_names = [collection.name for collection in collections]

        if collection_name not in collection_names:
            collection = client.create_collection(name=collection_name)
        else:
            collection = client.get_collection(name=collection_name)

        for idx, (embedding, text) in enumerate(zip(embeddings, texts)):
            embedding_id = f"embedding_{uuid.uuid4()}"
            try:
                collection.add(
                    ids=[embedding_id],
                    embeddings=[embedding],
                    metadatas=[{"text": text}]
                )
                print(f"Stored embedding with ID '{embedding_id}' for text: {text}")
            except Exception as e:
                print(f"Error adding embedding {embedding_id} to collection: {e}")
                continue

        print(f"All embeddings stored.")
    
    except Exception as e:
        print(f"Error accessing Chroma DB collection: {e}")

def generate_and_store_embeddings_with_ids(texts):
    embeddings = get_ai21_embeddings(texts)
    
    if embeddings:
        store_embeddings_with_ids(embeddings, texts)
    else:
        print("Failed to get embeddings from AI21. No embeddings stored.")

def read_texts_from_file(filename):
    texts = []
    try:
        with open(filename, 'r') as file:
            texts = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
    return texts

if __name__ == "__main__":
    filename = input("Enter the filename containing texts: ").strip()  
    texts = read_texts_from_file(filename)
    
    if texts:
        generate_and_store_embeddings_with_ids(texts)
    else:
        print("No texts were read from the file.")
