import os
import pandas as pd

from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS

from backend.rag.embeddings import get_embeddings


# ==========================================
# PATHS
# ==========================================

EXCEL_FILE = "data/excel/Organized_Notes_Report_Merged_With_Feedback.xlsx"
SAVE_PATH = "vectorstore/feedback_faiss"


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

for _, row in df.iterrows():

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
                page_content=text,
                metadata={
                    "source": "teacher_feedback"
                }
            )
        )

print(f"Created {len(documents)} documents")


# ==========================================
# CREATE EMBEDDINGS
# ==========================================

print("Loading embeddings...")

embeddings = get_embeddings()


# ==========================================
# CREATE FAISS INDEX
# ==========================================

print("Building FAISS index...")

vectorstore = FAISS.from_documents(
    documents,
    embeddings
)


# ==========================================
# SAVE FAISS
# ==========================================

os.makedirs(SAVE_PATH, exist_ok=True)

vectorstore.save_local(SAVE_PATH)

print(f"Saved FAISS index to: {SAVE_PATH}")

print("Done.")