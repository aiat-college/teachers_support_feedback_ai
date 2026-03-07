# backend/ingest/ingest_teacher.py

from backend.core.splitter import get_splitter
from backend.core.vectordb import build_vectordb
from backend.core.vectordb import get_vectorstore



def ingest_teacher_content(teacher_text: str):
    splitter = get_splitter()
    chunks = splitter.split_text(teacher_text)
    vectordb = build_vectordb(chunks)
    return vectordb
