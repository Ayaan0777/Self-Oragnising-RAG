from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Local Embeddings RAG Benchmarker")
app.include_router(router, prefix="/api/v1")