# Script Developer: Gabriel Mihai Sandu
# GitHub Profile: https://github.com/Gabrieliam42

import chromadb

chromaclient = chromadb.HttpClient(host="localhost", port=8000)

collections = chromaclient.list_collections()
print(f"Available Collections: {[col for col in collections]}")

if "Local_RAG_database" in collections:
    collection = chromaclient.get_collection(name="Local_RAG_database")
    
    docs = collection.peek()
    print(f"Total documents stored: {len(docs['documents'])}")

    for i, doc in enumerate(docs['documents'][:5]):
        print(f"\nDocument {i+1}: {doc}")
else:
    print("[ERROR] Collection 'Local_RAG_database' does not exist.")
