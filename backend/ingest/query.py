from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

FAISS_PATH = "data/faiss_index"

def run_query():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectordb = FAISS.load_local(
    FAISS_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

    print("✅ FAISS index loaded")

    while True:
        query = input("\n🔎 Enter your query (or 'exit'): ")
        if query.lower() == "exit":
            break

        results = vectordb.similarity_search(query, k=3)
        for i, r in enumerate(results, 1):
            print(f"\n--- Result {i} ---")
            print(r.page_content[:500])

if __name__ == "__main__":
    run_query()
