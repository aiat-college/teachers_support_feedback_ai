from backend.core.loader import load_pdfs
from backend.core.splitter import get_splitter
from backend.core.embeddings import get_embeddings
from backend.core.vectordb import get_vectorstore

def ingest_pdfs():
    documents = load_pdfs("data/pdfs")

    if not documents:
        raise ValueError("❌ No PDF documents loaded. Check data/pdfs folder.")

    splitter = get_splitter()
    docs = splitter.split_documents(documents)

    if not docs:
        raise ValueError("❌ Documents loaded but splitter returned 0 chunks.")

    print(f"✅ Loaded {len(documents)} PDFs")
    print(f"✂️ Created {len(docs)} chunks")

    embeddings = get_embeddings()
    vectordb = get_vectorstore(docs, embeddings)

    vectordb.save_local("data/faiss_index")
    print("💾 FAISS index saved to data/faiss_index")

if __name__ == "__main__":
    ingest_pdfs()
