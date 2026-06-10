from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaLLM

from backend.rag.embeddings import get_embeddings
from backend.rag.prompts import MENTOR_PROMPT

import faiss
import pickle
import numpy as np
import os
import re

# =====================================================
# PATHS
# =====================================================

BASE_VECTORSTORE_PATH = "vectorstore"

BOOKS_FAISS_PATH = os.path.join(BASE_VECTORSTORE_PATH, "books_faiss")
FEEDBACK_FAISS_PATH = os.path.join(BASE_VECTORSTORE_PATH, "feedback_faiss")
YOUTUBE_FAISS_PATH = os.path.join(BASE_VECTORSTORE_PATH, "youtube_faiss")
WEB_FAISS_PATH = os.path.join(BASE_VECTORSTORE_PATH, "web_faiss")

# =====================================================
# TEXT FORMATTER
# =====================================================
def format_vertical_text(text):

    # Remove extra spaces/newlines
    text = re.sub(r"\s+", " ", text).strip()

    # Display BOOK title separately
    if text.startswith("BOOK:"):

        first_newline = text.find("\n")

        if first_newline != -1:

            title = text[:first_newline].strip()
            body = text[first_newline:].strip()

            print(title)
            print()

            text = body

    # Split into readable sentences
    sentences = re.split(
        r'(?<=[.!?])\s+',
        text
    )

    for sentence in sentences:

        sentence = sentence.strip()

        if sentence:

            print(sentence)
            print()

# =====================================================
# LOAD EMBEDDINGS
# =====================================================

print("Loading Embeddings...")
embeddings = get_embeddings()

# =====================================================
# LOAD FEEDBACK FAISS
# =====================================================

#print("Loading Feedback FAISS...")

feedback_db = FAISS.load_local(
    FEEDBACK_FAISS_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

# =====================================================
# LOAD YOUTUBE FAISS
# =====================================================

#print("Loading YouTube FAISS...")

youtube_db = FAISS.load_local(
    YOUTUBE_FAISS_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

# =====================================================
# LOAD WEB FAISS
# =====================================================

#print("Loading Web FAISS...")

web_db = FAISS.load_local(
    WEB_FAISS_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

# =====================================================
# LOAD BOOKS FAISS
# =====================================================

#print("Loading Books FAISS...")

books_index = faiss.read_index(
    os.path.join(
        BOOKS_FAISS_PATH,
        "index.faiss"
    )
)

with open(
    os.path.join(
        BOOKS_FAISS_PATH,
        "index.pkl"
    ),
    "rb"
) as f:

    books_documents = pickle.load(f)

print(f"Books vectors loaded: {books_index.ntotal}")
print(f"Books documents loaded: {len(books_documents)}")

# =====================================================
# LOAD LLM
# =====================================================

#print("Loading Gemma...")

llm = OllamaLLM(
    model="gemma:2b"
)

#print("✅ GEMMA Ready")

# =====================================================
# TEACHER INPUT
# =====================================================

print("\n========== TEACHER REFLECTION ==========\n")

prepared = input("1. What I prepared?\n> ")

did_well = input(
    "\n2. What I did well?\n> "
)

went_well = input(
    "\n3. What went well?\n> "
)

improve = input(
    "\n4. Where to improve?\n> "
)

homework = input(
    "\n5. What homework did I give today?\n> "
)

# =====================================================
# HANDLE EMPTY
# =====================================================

if not improve.strip():
    improve = "Teacher did not identify improvement areas."

if not homework.strip():
    homework = "No homework assigned."

# =====================================================
# SEARCH QUERY
# =====================================================

search_query = f"""
Topic:
{prepared}

Teaching Success:
{did_well}

Student Response:
{went_well}

Improvement:
{improve}
"""

# =====================================================
# RETRIEVE DOCS
# =====================================================

print("\nSearching Knowledge Base...\n")

feedback_docs = []
youtube_docs = []
web_docs = []

# ---------------- FEEDBACK ----------------

try:

    feedback_docs = feedback_db.similarity_search(
        search_query,
        k=3
    )

except Exception as e:

    print(
        "Feedback Retrieval Error:",
        e
    )

# ---------------- YOUTUBE ----------------

try:

    youtube_docs = youtube_db.similarity_search(
        search_query,
        k=3
    )

except Exception as e:

    print(
        "YouTube Retrieval Error:",
        e
    )

# ---------------- WEB ----------------

try:

    web_docs = web_db.similarity_search(
        search_query,
        k=3
    )

except Exception as e:

    print(
        "Web Retrieval Error:",
        e
    )

# =====================================================
# BOOK SEARCH
# =====================================================

query_embedding = embeddings.embed_query(
    search_query
)

query_vector = np.array(
    [query_embedding],
    dtype=np.float32
)

distances, indices = books_index.search(
    query_vector,
    10
)

best_book = None

if len(indices[0]) > 0:

    idx = indices[0][0]

    if idx < len(books_documents):
        best_book = books_documents[idx]

# =====================================================
# BUILD CONTEXT
# =====================================================

feedback_context = "\n".join(
    [
        doc.page_content[:700]
        for doc in feedback_docs
    ]
)

youtube_context = "\n".join(
    [
        doc.page_content[:700]
        for doc in youtube_docs
    ]
)

web_context = "\n".join(
    [
        doc.page_content[:700]
        for doc in web_docs
    ]
)

book_context = ""

if best_book:

    book_context = getattr(
        best_book,
        "page_content",
        str(best_book)
    )

    if len(book_context) > 700:
        book_context = book_context[:700]

context = f"""
FEEDBACK EXAMPLES:
{feedback_context}

BOOK PEDAGOGY REFERENCES:
{book_context}

YOUTUBE TEACHING VIDEOS:
{youtube_context}

WEB EDUCATIONAL RESOURCES:
{web_context}
"""

# =====================================================
# QUESTION
# =====================================================

teacher_question = f"""
What I prepared:
{prepared}

What I did well:
{did_well}

What went well:
{went_well}

Where to improve:
{improve}

What homework did I give today:
{homework}
"""

# =====================================================
# PROMPT
# =====================================================

prompt = MENTOR_PROMPT.format(
    context=context,
    question=teacher_question
)

# =====================================================
# GENERATE RESPONSE
# =====================================================

print(
    "\nGenerating Mentor Feedback...\n"
)

response = llm.invoke(prompt)

# =====================================================
# DISPLAY FEEDBACK
# =====================================================

print(
    "\n========== MENTOR FEEDBACK ==========\n"
)

print(response)

# =====================================================
# RESOURCE DISPLAY
# =====================================================

print(
    "\n========== RECOMMENDED RESOURCES ==========\n"
)

resource_docs = []

if best_book:
    resource_docs.append(best_book)

if youtube_docs:
    resource_docs.append(youtube_docs[0])

if web_docs:
    resource_docs.append(web_docs[0])

if not resource_docs:

    print(
        "No relevant resources found."
    )

else:

    for i, doc in enumerate(
        resource_docs,
        start=1
    ):

        print(
            f"\nResource {i}"
        )

        print("-" * 50)

        if doc in youtube_docs:

            print(
                "🎥 YOUTUBE VIDEO RESOURCE"
            )

        elif doc in web_docs:

            print(
                "🌐 WEB RESOURCE"
            )

        else:

            print(
                "📘 BOOK RESOURCE"
            )

        text = getattr(
            doc,
            "page_content",
            str(doc)
        )

        if len(text) > 500:
            text = text[:500] + "..."

        format_vertical_text(text)

        metadata = getattr(
            doc,
            "metadata",
            {}
        )

        if metadata:

            if "source" in metadata:
                print(
                    "Source:",
                    metadata["source"]
                )

            if "url" in metadata:
                print(
                    "URL:",
                    metadata["url"]
                )

        print()