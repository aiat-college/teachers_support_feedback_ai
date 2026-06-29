import os
from pathlib import Path
import re
from pypdf import PdfReader

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

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

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =====================================
# READ PDF FILES
# =====================================
all_chunks = []

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

                all_chunks.append(
                    f"BOOK: {pdf_file}\n\n{chunk}"
                )

    except Exception as e:

        print(f"Error reading {pdf_file}")
        print(e)

print(f"\nTotal chunks created: {len(all_chunks)}")

# =====================================
# CREATE LANGCHAIN FAISS
# =====================================

print("\nCreating LangChain FAISS index...")

vectorstore = FAISS.from_texts(
    all_chunks,
    embeddings
)

# =====================================
# SAVE
# =====================================

SAVE_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)

vectorstore.save_local(
    str(SAVE_FOLDER)
)

print("\n✅ books vectorstore created successfully")
print(f"Saved at: {SAVE_FOLDER}")