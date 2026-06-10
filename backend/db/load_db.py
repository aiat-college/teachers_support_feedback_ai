from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

VECTORSTORE_PATH = "vectorstore_path"  # Change this to your actual saved vectorstore folder

def load_vectorstore():
    from langchain_community.vectorstores import FAISS
    from langchain_ollama import OllamaEmbeddings

    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    return FAISS.load_local(
        "vectorstore",   # ✅ correct folder name
        embeddings,
        allow_dangerous_deserialization=True
    )


# Optional: quick test
if __name__ == "__main__":
    db = load_vectorstore()
    print("Vectorstore loaded:", db)
