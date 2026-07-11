from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# =====================================
# PATHS
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# =====================================
# LOAD EMBEDDINGS
# =====================================

print("Loading embeddings...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =====================================
# LOAD VECTORSTORE
# =====================================

print("Loading books vectorstore...")

books_index = FAISS.load_local(
    str(BASE_DIR / "vectorstore" / "books"),
    embeddings,
    allow_dangerous_deserialization=True
)

print("Vectorstore loaded successfully!")

# =====================================
# TEST QUERY
# =====================================

query = "project based learning"

print(f"\nSearching for: {query}\n")

results = books_index.similarity_search(
    query,
    k=3
)

print(f"Found {len(results)} results\n")

for i, doc in enumerate(results, start=1):

    print("=" * 80)
    print(f"RESULT {i}")
    print("=" * 80)

    print(doc.page_content[:1500])

    print("\n")