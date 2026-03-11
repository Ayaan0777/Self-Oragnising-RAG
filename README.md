Step 1 - Install dependencies in a virtual environment
pip install fastapi uvicorn pydantic-settings langchain langchain-pinecone pinecone-client langchain-ollama langchain-google-genai ragas datasets

Step 2- Create an account in pinecone and an index with the dimensions of the embedding model used 
->Enter name of index
->Select Custom settings
->Enter dimensions

Step 3 - Create .env with content
PINECONE_API_KEY=API_KEY
PINECONE_INDEX_NAME=name_of_index

EMBEDDING_MODEL_NAME=model_name
OLLAMA_BASE_URL=http://localhost:11434

GEMINI_API_KEY=API_KEY
LLM_PROVIDER=ollama | gemini (depends on what you are using)
LLM_MODEL_NAME=ollama model name | gemini model name

Step 4- Upload the files on /ingest endpoint and query on /query endpoint , the thrid endpoint works only for cloud models as evaluation is not possible
 running through the local models







