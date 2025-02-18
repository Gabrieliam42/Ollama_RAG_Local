# Script Developer: Gabriel Mihai Sandu
# GitHub Profile: https://github.com/Gabrieliam42

import sys
import chromadb
import ollama

MODEL_NAME = "codellama:13b"

if len(sys.argv) < 2:
    print("Usage: python search.py 'Your query here'")
    sys.exit(1)

query = " ".join(sys.argv[1:])

print(f"[INFO] Using Ollama model: {MODEL_NAME}")

chromaclient = chromadb.HttpClient(host="localhost", port=8000)
collection = chromaclient.get_or_create_collection(name="Local_RAG_database")

queryembed = ollama.embed(model="nomic-embed-text", input=query)['embeddings']

relateddocs = '\n\n'.join(collection.query(query_embeddings=queryembed, n_results=10)['documents'][0])
prompt = f"{query} - Answer that question using the following text as a resource: {relateddocs}"

ragoutput = ollama.generate(model=MODEL_NAME, prompt=prompt, stream=False)
print(f"Answered with RAG ({MODEL_NAME}): {ragoutput['response']}")
print()
print()
print("---------------------------------------------------------------------------------------------")
print()
print()
noragoutput = ollama.generate(model=MODEL_NAME, prompt=query, stream=False)
print(f"Answered without RAG ({MODEL_NAME}): {noragoutput['response']}")
