import os
import faiss
import pickle
import numpy as np

from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# ==================================================
# PROJECT PATHS
# ==================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "..")
)

BOOKS_FOLDER = os.path.join(
    PROJECT_ROOT,
    "data",
    "books"
)

SAVE_FOLDER = os.path.join(
    PROJECT_ROOT,
    "vectorstore",
    "books_faiss"
)

CHUNK_SIZE = 1000

# ==================================================
# LOAD EMBEDDING MODEL
# ==================================================

print("Loading embedding model...")

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# ==================================================
# READ PDF FILES
# ==================================================

all_chunks = []

pdf_files = [
    file
    for file in os.listdir(BOOKS_FOLDER)
    if file.lower().endswith(".pdf")
]

print(f"Found {len(pdf_files)} PDF files")

for pdf_file in pdf_files:

    pdf_path = os.path.join(
        BOOKS_FOLDER,
        pdf_file
    )

    print(f"Reading: {pdf_file}")

    try:

        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:
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

        print(
            f"Error reading {pdf_file}"
        )

        print(e)

print(
    f"\nTotal chunks created: {len(all_chunks)}"
)

# ==================================================
# CREATE EMBEDDINGS
# ==================================================

print("\nCreating embeddings...")

embeddings = model.encode(
    all_chunks,
    show_progress_bar=True
)

embeddings = np.array(
    embeddings,
    dtype=np.float32
)

# ==================================================
# CREATE FAISS INDEX
# ==================================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(
    dimension
)

index.add(
    embeddings
)

# ==================================================
# CREATE OUTPUT FOLDER
# ==================================================

os.makedirs(
    SAVE_FOLDER,
    exist_ok=True
)

# ==================================================
# SAVE FAISS INDEX
# ==================================================

faiss.write_index(
    index,
    os.path.join(
        SAVE_FOLDER,
        "index.faiss"
    )
)

# ==================================================
# SAVE DOCUMENTS
# ==================================================

with open(
    os.path.join(
        SAVE_FOLDER,
        "documents.pkl"
    ),
    "wb"
) as f:

    pickle.dump(
        all_chunks,
        f
    )

# ==================================================
# DONE
# ==================================================

print(
    "\n✅ books_faiss created successfully"
)

print(
    f"Total chunks stored: {len(all_chunks)}"
)

print(
    f"Saved at: {SAVE_FOLDER}"
)