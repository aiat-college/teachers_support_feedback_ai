from langchain_community.vectorstores import FAISS

FAISS_PATH = "data/faiss_index"

def retrieve(vectorstore=None, query=None):
    # Load from FAISS if no vectorstore is provided
    if vectorstore is None:
        vectorstore = FAISS.load_local(FAISS_PATH)
    
    docs = vectorstore.similarity_search(query)
    return docs
