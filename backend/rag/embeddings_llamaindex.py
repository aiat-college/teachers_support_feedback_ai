from llama_index.embeddings.huggingface import HuggingFaceEmbedding

MODEL_NAME = "BAAI/bge-small-en-v1.5"


def get_embeddings():
    """
    Return LlamaIndex embedding model
    for FAISS loading and retrieval.
    """

    return HuggingFaceEmbedding(
        model_name=MODEL_NAME,
        normalize=True
    )