import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

# static knowledge base (can be upgraded later)
docs = [
    "Good communication improves teaching effectiveness",
    "Classroom control is important for discipline",
    "Interactive teaching improves student engagement",
    "Teachers should provide clear explanations",
]

def build_index():
    embeddings = model.encode(docs)
    embeddings = np.array(embeddings).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    return index, docs


def retrieve_context(index, docs, query, k=2):
    q_emb = model.encode([query]).astype("float32")

    D, I = index.search(q_emb, k)

    return "\n".join([docs[i] for i in I[0]])