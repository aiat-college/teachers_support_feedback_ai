from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import YoutubeLoader


import os

def load_pdfs(folder_path):   ##pdf_loader.py##
    documents = []

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(folder_path, file))
            documents.extend(loader.load())

    return documents

def load_support_video(url: str) -> str: ### Added the load_youtube function###
    """Load transcript from a YouTube video"""
    try:
        loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
        docs = loader.load()
        return "\n".join(doc.page_content for doc in docs)
    except Exception as e:
        print(f"❌ Failed to load {url}: {e}")
        return ""