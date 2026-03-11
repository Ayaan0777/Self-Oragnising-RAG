import os
import re
import tempfile
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from services.llm_factory import get_vector_store


def clean_text(text: str) -> str:
    """Removes newlines, tabs, and collapses multiple spaces into one."""
    cleaned = re.sub(r"\s+", " ", text)
    return cleaned.strip()


def process_and_store_file(file: UploadFile):
    print(f"\n--- 📥 STARTING INGESTION: {file.filename} ---")

    file_extension = os.path.splitext(file.filename)[1].lower()

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
        temp_file.write(file.file.read())
        temp_file_path = temp_file.name

    try:
        print(f"⏳ Extracting text from {file_extension}...")

        if file_extension == ".pdf":
            loader = PyPDFLoader(temp_file_path)

        elif file_extension == ".docx":
            loader = Docx2txtLoader(temp_file_path)

        elif file_extension == ".txt":
            loader = TextLoader(temp_file_path)

        else:
            return {"error": "Unsupported file type"}

        raw_documents = loader.load()

        # Clean text
        print("🧹 Cleaning text...")
        for doc in raw_documents:
            doc.page_content = clean_text(doc.page_content)

        print("✅ Text cleaning complete.")

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    print("✂️ Splitting into chunks...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = text_splitter.split_documents(raw_documents)

    print(f"📦 Generated {len(chunks)} chunks")

    # Connect to vector store
    vector_store = get_vector_store()

    print("🚀 Uploading chunks to Pinecone...")
    vector_store.add_documents(documents=chunks)

    print(f"🎉 SUCCESS: {file.filename} indexed!\n")

    return {
        "message": "Document ingested successfully",
        "chunks_created": len(chunks)
    }