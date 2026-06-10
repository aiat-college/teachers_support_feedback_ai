import os
from langchain_ollama import OllamaEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings  ## Added  import for youtubes
from langchain_community.vectorstores import FAISS

def build_vectordb(chunks):
    if not chunks:
        raise ValueError("❌ No chunks provided to build vector DB")

    embeddings = HuggingFaceEmbeddings()
    return FAISS.from_texts(chunks, embeddings)



def get_embeddings(): ## Added function to get ollama embeddings for pdf_loader###
    return OllamaEmbeddings(
        model="nomic-embed-text",
        base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
    )

