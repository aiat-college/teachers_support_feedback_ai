from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

BASE_DIR = Path(__file__).resolve().parent

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    str(BASE_DIR / "vectorstore" / "youtube"),
    embeddings,
    allow_dangerous_deserialization=True
)

results = db.similarity_search(
    "place value teaching",
    k=3
)

for r in results:
    print("=" * 80)
    print(r.page_content)