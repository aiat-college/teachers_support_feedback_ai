from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain_ollama import OllamaEmbeddings



def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def build_vectordb(chunks):
    if not chunks:
        raise ValueError("❌ No text chunks provided to build vector DB")

    embeddings = HuggingFaceEmbeddings()
    return FAISS.from_texts(chunks, embeddings)

def get_vectorstore(docs, embeddings):
    if not docs:
        raise ValueError("❌ No documents provided to build vector DB")

    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    vectordb = FAISS.from_documents(docs, embeddings)

    return vectordb

def create_vectorstore(docs):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.from_texts(docs, embeddings)