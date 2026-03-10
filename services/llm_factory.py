from langchain_ollama import OllamaEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from pinecone import Pinecone
from config import settings

# Initialize Pinecone
pc = Pinecone(api_key=settings.pinecone_api_key)

def get_embeddings():
    """Returns the local Ollama embedding instance."""
    return OllamaEmbeddings(
        model=settings.embedding_model_name,
        base_url=settings.ollama_base_url
    )

def get_llm():
    """Returns the cloud Gemini LLM instance."""
    return ChatGoogleGenerativeAI(
        model=settings.llm_model_name,
        google_api_key=settings.gemini_api_key,
        temperature=0.2
    )


def get_vector_store():
    """Connects to Pinecone using the local Ollama embedding model."""
    return PineconeVectorStore(
        index_name=settings.pinecone_index_name, 
        embedding=get_embeddings(),
        pinecone_api_key=settings.pinecone_api_key  # <-- Add this exact line
    )