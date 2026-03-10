from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    pinecone_api_key: str
    pinecone_index_name: str
    
    embedding_model_name: str = "bge-m3"
    ollama_base_url: str = "http://localhost:11434"
    
    gemini_api_key: str
    llm_model_name: str = "gemini-2.5-flash"

    class Config:
        env_file = ".env"

settings = Settings()