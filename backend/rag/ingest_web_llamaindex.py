import os

from llama_index.readers.web import SimpleWebPageReader
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.faiss import FaissVectorStore

import faiss

from backend.rag.embeddings_llamaindex import get_embeddings

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

        docs = SimpleWebPageReader(html_to_text=True).load_data([url])

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

splitter = SentenceSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

nodes = splitter.get_nodes_from_documents(documents)

print(f"Created {len(nodes)} chunks")

# =====================================================
# CREATE FAISS INDEX
# =====================================================

embed_model = get_embeddings()

embedding_dim = len(embed_model.get_text_embedding("dimension probe"))

faiss_index = faiss.IndexFlatL2(embedding_dim)
vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

web_index = VectorStoreIndex(
    nodes,
    storage_context=storage_context,
    embed_model=embed_model
)

# =====================================================
# SAVE
# =====================================================

save_path = "vectorstore/web"

os.makedirs(save_path, exist_ok=True)

web_index.storage_context.persist(persist_dir=save_path)

print(f"\nSaved FAISS index to: {save_path}")