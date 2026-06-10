from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_vectorstore(texts):
    embeddings = model.encode(texts)

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))

    return index, embeddings, texts


def retrieve(query, index, texts, k=3):
    q_embed = model.encode([query])
    D, I = index.search(np.array(q_embed), k)

    return [texts[i] for i in I[0]]