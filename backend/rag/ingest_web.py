import os
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

from backend.rag.embeddings import get_embeddings

# =====================================================
# EDUCATIONAL WEB URLS
# =====================================================

URLS = [
    "https://www.auraauro.com/stem-land/teachers-support-website/"
]

# =====================================================
# LOAD WEB DOCUMENTS
# =====================================================

documents = []

for url in URLS:
    try:
        print(f"Loading: {url}")

        loader = WebBaseLoader(url)
        docs = loader.load()

        for doc in docs:
            doc.metadata["source"] = url

        documents.extend(docs)

    except Exception as e:
        print(f"Failed: {url}")
        print(e)

print(f"\nLoaded {len(documents)} web documents")

# =====================================================
# SPLIT DOCUMENTS
# =====================================================

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks")

# =====================================================
# CREATE FAISS INDEX
# =====================================================

embeddings = get_embeddings()

vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)

# =====================================================
# SAVE
# =====================================================

save_path = "vectorstore/web_faiss"

os.makedirs(os.path.dirname(save_path), exist_ok=True)

vectorstore.save_local(save_path)

print(f"\nSaved FAISS index to: {save_path}")