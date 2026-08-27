import os
from pathlib import Path
import re
from pypdf import PdfReader

import faiss
from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.faiss import FaissVectorStore

# =====================================
# PATHS
# =====================================

CURRENT_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = CURRENT_DIR.parent.parent

BOOKS_FOLDER = PROJECT_ROOT / "data" / "books"

SAVE_FOLDER = PROJECT_ROOT / "vectorstore" / "books"

CHUNK_SIZE = 1000

# =====================================
# LOAD EMBEDDING MODEL
# =====================================

print("Loading embedding model...")

embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Determine embedding dimension for FAISS index
EMBED_DIM = len(embed_model.get_text_embedding("dimension probe"))

# =====================================
# READ PDF FILES
# =====================================
all_docs = []

pdf_files = [
    file
    for file in os.listdir(BOOKS_FOLDER)
    if file.lower().endswith(".pdf")
]

print(f"Found {len(pdf_files)} PDF files")

for pdf_file in pdf_files:

    pdf_path = BOOKS_FOLDER / pdf_file

    print(f"Reading: {pdf_file}")

    try:

        reader = PdfReader(str(pdf_path))

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                page_text = page_text.replace("\xa0", " ")
                page_text = page_text.replace("\u2002", " ")
                page_text = page_text.replace("\u2003", " ")
                page_text = page_text.replace("\u2009", " ")

                page_text = re.sub(r"\s+", " ", page_text)

                text += page_text + "\n"

        # Chunking

        for i in range(
            0,
            len(text),
            CHUNK_SIZE
        ):

            chunk = text[
                i : i + CHUNK_SIZE
            ].strip()

            if len(chunk) > 50:

                all_docs.append(
                    Document(
                        text=chunk,
                        metadata={"book": pdf_file},
                    )
                )

    except Exception as e:

        print(f"Error reading {pdf_file}")
        print(e)

print(f"\nTotal chunks created: {len(all_docs)}")

# =====================================
# CREATE LLAMAINDEX FAISS INDEX
# =====================================

print("\nCreating LlamaIndex FAISS index...")

faiss_index = faiss.IndexFlatL2(EMBED_DIM)
vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    all_docs,
    storage_context=storage_context,
    embed_model=embed_model,
)

# =====================================
# SAVE
# =====================================

SAVE_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

index.storage_context.persist(persist_dir=str(SAVE_FOLDER))

print("\n✅ books vectorstore created successfully")
print(f"Saved at: {SAVE_FOLDER}")
