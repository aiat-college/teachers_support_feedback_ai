import os
import faiss
import pandas as pd

from llama_index.core import Document, VectorStoreIndex, StorageContext
from llama_index.vector_stores.faiss import FaissVectorStore

from backend.rag.embeddings_llamaindex import get_embeddings


# ==========================================
# PATHS
# ==========================================

EXCEL_FILE = "data/excel/Organized_Notes_Report_Merged_With_Feedback.xlsx"
SAVE_PATH = "vectorstore/feedback"


# ==========================================
# LOAD EXCEL
# ==========================================

print("Loading Excel file...")

df = pd.read_excel(EXCEL_FILE)

print(f"Loaded {len(df)} rows")


# ==========================================
# BUILD DOCUMENTS
# ==========================================

documents = []

columns = [
    "What_I_prepared",
    "What_I_did_well",
    "What_went_well",
    "Where_to_improve",
    "What_homework_did_I_give_today",
    "Feedback"
]

for idx, row in df.iterrows():

    content = []

    for col in columns:

        if col in df.columns:

            value = row.get(col)

            if pd.notna(value):
                content.append(f"{col}: {value}")

    text = "\n".join(content).strip()

    if text:

        documents.append(
            Document(
                text=text,
                metadata={
                    "source": "teacher_feedback",
                    "row_index": int(idx)
                }
            )
        )

print(f"Created {len(documents)} documents")


# ==========================================
# LOAD EMBEDDINGS
# ==========================================

print("Loading embeddings...")

embed_model = get_embeddings()


# ==========================================
# CREATE FAISS INDEX
# ==========================================

print("Building FAISS index...")

# Determine embedding dimension from the embed model
sample_vector = embed_model.get_text_embedding("dimension probe")
dimension = len(sample_vector)

faiss_index = faiss.IndexFlatL2(dimension)

vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    documents,
    storage_context=storage_context,
    embed_model=embed_model
)


# ==========================================
# SAVE FAISS
# ==========================================

os.makedirs(SAVE_PATH, exist_ok=True)

index.storage_context.persist(persist_dir=SAVE_PATH)

print(f"Saved FAISS index to: {SAVE_PATH}")

print("Done.")