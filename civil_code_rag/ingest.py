import os
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from config import DATA_PATH, DB_PATH, EMBEDDING_MODEL_NAME

def ingest_data():
    """Loads data, splits it, and creates a vector store."""
    if not os.path.exists(DATA_PATH):
        print(f"Error: Data file not found at {DATA_PATH}")
        return

    print(f"Loading data from {DATA_PATH}...")
    loader = Docx2txtLoader(DATA_PATH)
    documents = loader.load()
    print(f"Loaded {len(documents)} document(s).")

    print("Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", "。", "；", "，", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    print(f"Creating vector store at {DB_PATH}...")
    
    # Note: DashScopeEmbeddings will automatically use DASHSCOPE_API_KEY from os.environ
    # which is loaded by config.py
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=DashScopeEmbeddings(model=EMBEDDING_MODEL_NAME),
        persist_directory=DB_PATH
    )
    print("Vector store created and persisted.")

if __name__ == "__main__":
    ingest_data()
