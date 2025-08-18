import os
import sys
import ctypes
import subprocess
import tkinter as tk
from tkinter import messagebox
import fitz
import chromadb
import ollama

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def relaunch_as_admin():
    script = os.path.abspath(sys.argv[0])
    params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
    python_exe = sys.executable
    cmd_params = f'/k "{python_exe} \"{script}\" {params}"'
    ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", cmd_params, None, 1)
    sys.exit(0)

def extract_text_chunks_from_pdfs(directory, chunk_size=100):
    chunks = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".pdf"):
                filepath = os.path.join(root, file)
                try:
                    doc = fitz.open(filepath)
                    text_parts = []
                    for page in doc:
                        try:
                            text_parts.append(page.get_text("text") or "")
                        except Exception:
                            pass
                    full_text = " ".join(text_parts).strip()
                    if not full_text:
                        continue
                    words = full_text.split()
                    for i in range(0, len(words), chunk_size):
                        chunk = " ".join(words[i:i+chunk_size]).strip()
                        if chunk:
                            chunks.append((filepath, chunk))
                except Exception as e:
                    print(f"[ERROR] Could not process PDF {filepath}: {e}")
    return chunks

def create_embeddings(chunks):
    inputs = [c[1] for c in chunks]
    if not inputs:
        return []
    try:
        resp = ollama.embed(model="nomic-embed-text", input=inputs)
        embeds = resp.get("embeddings") or resp.get("data") or []
        if isinstance(embeds, dict) and "embeddings" in embeds:
            embeds = embeds["embeddings"]
        return embeds
    except Exception as e:
        print(f"[ERROR] Ollama embedding failed: {e}")
        return [[] for _ in inputs]

def build_chromadb_collection(chunks, embeddings):
    try:
        chromaclient = chromadb.HttpClient(host="localhost", port=8000)
    except Exception as e:
        raise RuntimeError(f"Failed to connect to ChromaDB HTTP service: {e}")
    try:
        existing = chromaclient.list_collections() or []
    except Exception:
        existing = []
    if "Local_RAG_database" in existing:
        try:
            chromaclient.delete_collection("Local_RAG_database")
        except Exception as e:
            print(f"[WARN] Could not delete existing collection: {e}")
    try:
        collection = chromaclient.get_or_create_collection(name="Local_RAG_database", metadata={"hnsw:space": "cosine"})
    except Exception as e:
        raise RuntimeError(f"Failed to create or get collection: {e}")
    ids = [f"{os.path.basename(src)}_{i}" for i, (src, _) in enumerate(chunks)]
    documents = [text for _, text in chunks]
    metadatas = [{"source": src} for src, _ in chunks]
    try:
        collection.add(ids=ids, documents=documents, embeddings=embeddings, metadatas=metadatas)
    except Exception as e:
        raise RuntimeError(f"Failed to add documents to collection: {e}")
    return collection

def main():
    root = tk.Tk()
    root.withdraw()
    cwd = os.getcwd()
    try:
        messagebox.showinfo("RAG Builder", f"Scanning directory:\n{cwd}")
    except Exception:
        pass
    try:
        chunks = extract_text_chunks_from_pdfs(cwd)
    except Exception as e:
        messagebox.showerror("Error", f"Failed during PDF scanning: {e}")
        return
    if not chunks:
        messagebox.showerror("Error", "No PDF files with extractable text were found in the current directory.")
        return
    try:
        embeddings = create_embeddings(chunks)
    except Exception as e:
        messagebox.showerror("Error", f"Embedding step failed: {e}")
        return
    try:
        build_chromadb_collection(chunks, embeddings)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to build ChromaDB collection: {e}")
        return
    try:
        messagebox.showinfo("Success", "ChromaDB collection 'Local_RAG_database' built successfully.")
    except Exception:
        pass

if __name__ == "__main__":
    if not is_admin():
        relaunch_as_admin()
    main()
