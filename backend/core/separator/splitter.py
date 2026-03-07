# backend/core/splitter.py

from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_splitter(chunk_size=1000, chunk_overlap=200):
    """
    Central text splitter used by PDF, TXT, YouTube, etc.
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
