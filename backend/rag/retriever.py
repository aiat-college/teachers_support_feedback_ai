from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

FAISS_PATH = "data/faiss_index"
embeddings = OllamaEmbeddings(model="nomic-embed-text")

def retrieve(vectorstore=None, query=None):
    # Load from FAISS if no vectorstore is provided
    if vectorstore is None:
        vectorstore = FAISS.load_local(FAISS_PATH,embeddings,allow_dangerous_deserialization=True)
    
    docs = vectorstore.similarity_search(query)
    return docs
