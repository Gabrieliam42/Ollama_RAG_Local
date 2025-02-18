# Ollama_RAG_Local

###### Ollama RAG with Local Data

##### This script has been tested on the Windows environment.
#

##### Prerequisites:

- Python 3.10 or later
- Docker
#

##### Requirements:

- `chromadb==0.6.2`
- `ollama`




<br><br>





<br><br>

#### Usage:

1. Run chromadb in Docker with the following cmd command:

`docker run -d -p 8000:8000 --gpus all --name chromadb chromadb/chroma:0.6.2`
2. Create a directory named "Local_RAG_data" in the project directory
3. Copy your local text data files (.txt) in the "Local_RAG_data" directory
4. Run "import_Local_RAG_data.py" and wait for it to chunk the text and to create the vector store database in chromadb
5. Ask Ollama RAG a question by using: python runRAG.py "Your query here" (Replace "Your query here" with your actual question or task)

You can use "test_chromadb.py" to check if chromadb is running and that the database has been created inside it.

<br><br>





<br><br>


**Script Developer:** Gabriel Mihai Sandu  
**GitHub Profile:** [https://github.com/Gabrieliam42](https://github.com/Gabrieliam42)
