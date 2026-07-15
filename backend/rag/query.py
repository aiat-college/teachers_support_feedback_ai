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
    docs = vectorstore.similarity_search(query, k=4)

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
# LEARNING RESOURCE RETRIEVAL
# =====================================
def retrieve_learning_resources(query):
    """
    Retrieve learning materials from all available vector stores.
    """

    print("\n===== RETRIEVING LEARNING RESOURCES =====")
    print("Query:", query)

    resources = {}

    # -----------------------------------
    # Books
    # -----------------------------------
    try:
        books_context = search_index(
            books_index,
            query
        )[:1200]

        resources["books"] = books_context

    except Exception as e:
        print("Books Search Error:", e)
        resources["books"] = ""

    # -----------------------------------
    # Mentor Feedback Examples
    # -----------------------------------
    try:
        feedback_context = search_index(
            feedback_index,
            query
        )[:1200]

        resources["feedback"] = feedback_context

    except Exception as e:
        print("Feedback Search Error:", e)
        resources["feedback"] = ""

    # -----------------------------------
    # Website (Enable later)
    # -----------------------------------
    """
    try:
        web_context = search_index(
            web_index,
            query
        )[:500]

        resources["web"] = web_context

    except Exception as e:
        print("Website Search Error:", e)
        resources["web"] = ""
    """

    # -----------------------------------
    # YouTube
    # -----------------------------------
    try:
        youtube_context = get_top_youtube_videos(
            youtube_index,
            query
        )

        resources["youtube"] = youtube_context

    except Exception as e:
        print("YouTube Search Error:", e)
        resources["youtube"] = ""

    print("\n===== RESOURCE SUMMARY =====")

    for source, value in resources.items():
        print(f"{source}: {len(value)} characters")

    print("===================================")

    return resources
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
# KEYWORD EXTRACTION
# =====================================
def extract_keywords(feedback):

    print("\n===== EXTRACTING KEYWORDS =====")

    prompt = f"""
{KEYWORD_EXTRACTION_PROMPT}

Mentor Feedback:

{feedback}
"""

    try:

        start = time.time()

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:latest", 
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 250,
                },
            },
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        keywords = data.get("response", "").strip()

        print("LLM Time:", round(time.time() - start, 2), "seconds")

        print("\n===== EXTRACTED KEYWORDS =====")
        print(keywords)

        return keywords

    except requests.exceptions.Timeout:
        print("Keyword extraction timed out.")
        return ""

    except Exception as e:
        import traceback

        traceback.print_exc()
        print("Keyword extraction failed:", e)
        return ""
    
# =====================================
# FEEDBACK GENERATION
# =====================================
def generate_teacher_feedback(
    grade,
    teacher,
    teacher_entries,
    notes_count
):
    """
    Generate mentor feedback for one teacher.
    """

    print(f"\nGenerating feedback for: {teacher}")

    prompt = f"""
{MENTOR_FEEDBACK_PROMPT}

Teacher Name: {teacher}
Grade: {grade}
Notes Count: {notes_count}

IMPORTANT RULES:
1. The teacher name is exactly "{teacher}".
2. Never change the teacher name.
3. Never invent another teacher.
4. Never change the grade.
5. Never change the notes count.
6. Use only the teacher reflections below.

Teacher Reflections:

{teacher_entries}

Your output MUST start exactly like this:

Grade {grade}, {teacher}, NotesCount={notes_count}
"""

    print("=" * 80)
    print("Teacher:", teacher)
    print("Grade:", grade)
    print("Teacher Entries Length:", len(teacher_entries))
    print("Notes Count:", notes_count)
    print("Prompt Length:", len(prompt))
    print("=" * 80)

    with open("debug_prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)

    try:

        start = time.time()

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3:latest",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 250,
                },
            },
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        feedback = data.get("response", "").strip()

        print("\n===== FEEDBACK GENERATED =====")
        print(feedback)
        print("LLM Time:", round(time.time() - start, 2), "seconds")

        if not feedback:
            return "Unable to generate feedback."

        # -----------------------------------
        # Extract Keywords
        # -----------------------------------
        keywords = extract_keywords(feedback)

        print("\n===== KEYWORDS =====")
        print(keywords)

        # -----------------------------------
        # Retrieve Learning Resources
        # -----------------------------------
        resources = retrieve_learning_resources(keywords)

        books_context = resources.get("books", "")
        feedback_context = resources.get("feedback", "")
        youtube_videos = resources.get("youtube", "")

        # (Future)
        # web_context = resources.get("web", "")

        print("\n===== BOOKS =====")
        print(books_context)

        print("\n===== FEEDBACK REFERENCES =====")
        print(feedback_context)

        print("\n===== YOUTUBE VIDEOS =====")
        print(youtube_videos)

        # -----------------------------------
        # Final Output
        # -----------------------------------
        final_output = f"""
        {feedback}

        ==================================================

        Recommended Reading

        Books:
        {books_context}

        --------------------------------------------------

        Mentor Feedback Examples:
        {feedback_context}

        ==================================================

        Recommended Videos

        {youtube_videos}
        """
         
        return final_output.strip()

    except requests.exceptions.Timeout:

        print("Feedback generation timed out.")
        return "Feedback generation timed out."

    except Exception as e:

        import traceback
        traceback.print_exc()

        return f"Error generating feedback: {str(e)}"
