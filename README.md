## Ollama Retrieval-Augmented Generation system with your Local Data

###### This project implements a system of RAG (Retrieval-Augmented Generation) that works with Ollama, with the Local Data you feed it.

##### The script has been tested on Windows.
#

##### Prerequisites:

- Python 3.10 or later
- Docker
- Ollama `https://ollama.com/download` or (`docker create --name ollama -p 11434:11434 --gpus all ollama/ollama`)
- ChromaDB `docker run -d --name Chromadb -p 8000:8000 --gpus=all -v ./chroma:/chroma/chroma -e IS_PERSISTENT=FALSE chromadb/chroma:0.6.2`
#

##### Requirements:

- `chromadb==0.6.2`
- `ollama`












<br><br>





<br><br>












#### Usage:

1. Run chromadb in Docker with the following cmd command:

   `docker run -d -p 8000:8000 --gpus all --name chromadb chromadb/chroma:0.6.2`

2. Run Ollama and install text embedding model by running this command in cmd: `ollama pull nomic-embed-text`

3. Create a directory named `Local_RAG_data` in the project directory

4. Copy your local text data files (.txt) in the `Local_RAG_data` directory

5. Run `import_Local_RAG_data.py` and wait for it to chunk the text, and it will then create the vector store database in chromadb

6. Ask Ollama RAG a question in the terminal by using: `python runRAG.py "Your query here"` (Replace "Your query here" with your actual question or task)

You can use `test_chromadb.py` to check if chromadb is running and that the database has been created inside it.
Also you can enter `http://localhost:8000/docs` to access the chromadb API.


<br><br>





<br><br>


**Script Developer:** Gabriel Mihai Sandu  
**GitHub Profile:** [https://github.com/Gabrieliam42](https://github.com/Gabrieliam42)
