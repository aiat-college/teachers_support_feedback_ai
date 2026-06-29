# backend/rag/query.py
from pathlib import Path
import requests
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import re
import time

from backend.rag.prompts import (
    MENTOR_FEEDBACK_PROMPT,
    KEYWORD_EXTRACTION_PROMPT,
)
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# =====================================
# PATHS
# =====================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# =====================================
# EMBEDDINGS
# =====================================

print("Loading embeddings...")
# =====================================
# LOAD VECTORSTORES
# =====================================

print("Loading vectorstores...")

books_index = FAISS.load_local(
    str(BASE_DIR / "vectorstore" / "books"),
    embeddings,
    allow_dangerous_deserialization=True
)

feedback_index = FAISS.load_local(
    str(BASE_DIR / "vectorstore" / "feedback"),
    embeddings,
    allow_dangerous_deserialization=True
)


#web_index = FAISS.load_local(
    #str(BASE_DIR / "vectorstore" / "web"),
    #embeddings,
    #allow_dangerous_deserialization=True
#)
youtube_index = FAISS.load_local(
    str(BASE_DIR / "vectorstore" / "youtube"),
    embeddings,
    allow_dangerous_deserialization=True
)
print("All vectorstores loaded successfully.")

# =====================================
# SEARCH
# =====================================

def search_index(vectorstore, query):
    docs = vectorstore.similarity_search(query, k=2)

    return "\n\n".join(
        doc.page_content[:1000]
        for doc in docs
    )
# YOUTUBE RANKED SEARCH
def search_youtube_ranked(vectorstore, query, k=5):

    docs_with_scores = vectorstore.similarity_search_with_score(
        query,
        k=k
    )

    print("\n===== RAW YOUTUBE SEARCH RESULTS =====")
    print("Query:", query)

    results = []

    for doc, score in docs_with_scores:

        print("\nScore:", score)
        print(doc.page_content[:300])

        results.append({
            "content": doc.page_content,
            "score": score
        })

    print("Total Results:", len(results))

    return results


# =====================================
# CONTEXT RETRIEVAL
# =====================================

def retrieve_context(query):

    books_context = search_index(
        books_index,
        query
    )[:300]

    feedback_context = search_index(
        feedback_index,
        query
    )[:300]

    youtube_results = search_youtube_ranked(
        youtube_index,
        query
    )

    youtube_context = "\n\n".join(
        item["content"][:250]
        for item in youtube_results[:2]
    )

    context = f"""
BOOKS:
{books_context}

FEEDBACK:
{feedback_context}

YOUTUBE:
{youtube_context}
"""

    print("Context Length:", len(context))
    # print(prompt[:2000])
    return context
def extract_youtube_info(text):

    title = "Unknown Title"
    url = "No URL found"

    title_match = re.search(r"Title:\s*(.*)", text)
    url_match = re.search(r"(https?://[^\s]+)", text)

    if title_match:
        title = title_match.group(1)

    if url_match:
        url = url_match.group(1)

    return title, url

def get_top_youtube_videos(vectorstore, query):

    results = search_youtube_ranked(vectorstore, query)

    # Keep only relevant results
    filtered = []

    for item in results:

        score = item["score"]
        print("SCORE =", item["score"])
        # Adjust this value after testing
        if score < 0.8:
            filtered.append(item)

    if not filtered:
        return "No relevant videos found."

    output = []

    for item in filtered[:3]:

        text = item["content"]

        title, url = extract_youtube_info(text)

        output.append(
            f"🎥 {title}\n🔗 {url}"
        )

    return "\n\n".join(output)

# =====================================
# FEEDBACK GENERATION
# =====================================
def generate_teacher_feedback(
    teacher,
    teacher_entries,
    notes_count
):

    print(f"Generating feedback for: {teacher}")

    prompt = f"""
{MENTOR_FEEDBACK_PROMPT}

Teacher Name:
{teacher}

Notes Count:
{notes_count}

Teacher Reflection:
{teacher_entries}
"""

    print("\n===== PROMPT PREVIEW =====")
    print(prompt[:3000])

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:latest",
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 250,
                "temperature": 0.3
            }
        },
        timeout=300
    )

    response.raise_for_status()
    feedback = response.json()["response"].strip()

    print("\n===== GENERATED FEEDBACK =====")
    print(feedback)

    return feedback

    return response.json()["response"]
# =====================================
# KEYWORD EXTRACTION
# =====================================

def extract_keywords(feedback):

    print("\n===== EXTRACTING KEYWORDS =====")

    prompt = f"""
{KEYWORD_EXTRACTION_PROMPT}

Mentor Feedback:

{feedback}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:latest",
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": 100,
                "temperature": 0.2
            }
        },
        timeout=300
    )

    response.raise_for_status()

    keywords = response.json()["response"].strip()

    print("\n===== EXTRACTED KEYWORDS =====")
    print(keywords)

    return keywords
