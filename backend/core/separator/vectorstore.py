import os
from langchain_community.vectorstores import FAISS
from core.embeddings import get_embeddings

FAISS_PATH = "data/faiss_index"

def create_vectorstore(docs):
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    
    # Ensure folder exists
    os.makedirs(FAISS_PATH, exist_ok=True)
    
    vectorstore.save_local(FAISS_PATH)
    return vectorstore