from langchain_huggingface import HuggingFaceEmbeddings

MODEL_NAME = "BAAI/bge-small-en-v1.5"


def get_embeddings():
    """
    Return LangChain embedding model
    for FAISS loading and retrieval.
    """

    return HuggingFaceEmbeddings(
        model_name=MODEL_NAME,
        encode_kwargs={
            "normalize_embeddings": True
        }
    )