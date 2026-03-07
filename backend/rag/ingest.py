import os
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain.schema import Document

DATA_PATH = "backend/data"
VECTOR_PATH = "vectorstore"

def create_vectorstore():
    documents = []

    for file in os.listdir(DATA_PATH):
        with open(os.path.join(DATA_PATH, file), "r", encoding="utf-8") as f:
            documents.append(Document(page_content=f.read()))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    db = FAISS.from_documents(chunks, embeddings)
    db.save_local(VECTOR_PATH)

    print("✅ Vector DB created successfully")

if __name__ == "__main__":
    create_vectorstore()
