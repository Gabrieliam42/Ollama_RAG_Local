# Script Developer: Gabriel Mihai Sandu
# GitHub Profile: https://github.com/Gabrieliam42

import os
import re
import ollama
import chromadb

def readtextfiles(path):
    text_contents = {}

    for root, _, files in os.walk(path):
        for filename in files:
            if filename.endswith(".txt"):
                file_path = os.path.join(root, filename)

                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()

                text_contents[file_path] = content

    return text_contents

def chunksplitter(text, chunk_size=100):
    words = re.findall(r'\S+', text)

    chunks = []
    current_chunk = []
    word_count = 0

    for word in words:
        current_chunk.append(word)
        word_count += 1

        if word_count >= chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            word_count = 0

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def getembedding(chunks):
    embeds = ollama.embed(model="nomic-embed-text", input=chunks)
    return embeds.get('embeddings', [])

chromaclient = chromadb.HttpClient(host="localhost", port=8000)
textdocspath = "Local_RAG_data"

if not os.path.exists(textdocspath):
    os.makedirs(textdocspath)
    print(f"[INFO] Created missing directory: {textdocspath}")

print("[INFO] Reading text files...")
text_data = readtextfiles(textdocspath)
print(f"[INFO] Found {len(text_data)} text files.")

if "Local_RAG_database" in chromaclient.list_collections():
    print("[INFO] Deleting existing collection...")
    chromaclient.delete_collection("Local_RAG_database")

collection = chromaclient.get_or_create_collection(name="Local_RAG_database", metadata={"hnsw:space": "cosine"})
print("[INFO] Created new collection.")

for filename, text in text_data.items():
    print(f"[INFO] Processing file: {filename}")
    
    chunks = chunksplitter(text)
    print(f"[INFO] Split into {len(chunks)} chunks.")

    embeds = getembedding(chunks)
    print(f"[INFO] Generated {len(embeds)} embeddings.")

    chunknumber = list(range(len(chunks)))
    ids = [filename + str(index) for index in chunknumber]
    metadatas = [{"source": filename} for _ in chunknumber]

    collection.add(ids=ids, documents=chunks, embeddings=embeds, metadatas=metadatas)
    print(f"[INFO] Added {len(chunks)} chunks to ChromaDB.")

print("[SUCCESS] Data import completed.")
