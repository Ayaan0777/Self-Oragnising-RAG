import os
import tempfile
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from services.llm_factory import get_vector_store

def process_and_store_file(file: UploadFile):
    # 1. Extract the file extension
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    # 2. Save the uploaded file to a temporary system directory
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        temp_file.write(file.file.read())
        temp_file_path = temp_file.name

    try:
        # 3. Route to the correct LangChain loader
        if file_extension == ".pdf":
            loader = PyPDFLoader(temp_file_path)
        elif file_extension == ".docx":
            loader = Docx2txtLoader(temp_file_path)
        elif file_extension == ".txt":
            loader = TextLoader(temp_file_path)
        else:
            return {"error": f"Unsupported file type: {file_extension}. Use pdf, docx, or txt."}
        
        # Extract the text into LangChain Document objects
        documents = loader.load()
        
    finally:
        # 4. CRITICAL: Always delete the temp file from the server, even if the loader fails
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    # 5. Chunk and store the documents
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)
    
    vector_store = get_vector_store()
    # Note: We use add_documents() now instead of add_texts()
    vector_store.add_documents(documents=chunks) 
    
    return {
        "message": f"Successfully ingested {len(chunks)} chunks from {file.filename}."
    }