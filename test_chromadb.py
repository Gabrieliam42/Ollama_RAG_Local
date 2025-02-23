# Script Developer: Gabriel Mihai Sandu
# GitHub Profile: https://github.com/Gabrieliam42

import chromadb

client = chromadb.HttpClient(host="localhost", port=8000)

collections = client.list_collections()
print("Available collections:", collections)

for collection_name in collections:
    collection = client.get_collection(collection_name)
    print(f"Collection: {collection.name}")
