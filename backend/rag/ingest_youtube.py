import os
import pickle

from googleapiclient.discovery import build

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from backend.rag.embeddings import get_embeddings

# =====================================================
# CONFIG
# =====================================================

YOUTUBE_API_KEY = "AIzaSyBjEQPDR4oxw8cOV1D_MdsjkyZbFWyekVM"

YOUTUBE_CHANNELS = [
    "UCnaq8X41wWMlTdFw70-M8dQ",
    "UCE4evifjDjoOMzNfT8PQN2A"
]

BASE_VECTORSTORE_PATH = "vectorstore"

YOUTUBE_FAISS_PATH = os.path.join(
    BASE_VECTORSTORE_PATH,
    "youtube_faiss"
)

os.makedirs(YOUTUBE_FAISS_PATH, exist_ok=True)

# =====================================================
# SUNDRAM RECORDINGS
# =====================================================

SUNDRAM_RECORDINGS = [

    {
        "title": "Place Value Session 1",
        "topic": "place value",
        "keywords": [
            "place value",
            "ones",
            "tens",
            "hundreds",
            "number sense"
        ],
        "date": "20/06/2020",
        "url": "https://youtu.be/wXG1F5nyLyY"
    },

    {
        "title": "Place Value Session 2",
        "topic": "place value",
        "keywords": [
            "place value",
            "expanded form",
            "ones",
            "tens"
        ],
        "date": "20/06/2020",
        "url": "https://youtu.be/ySa-8k5UnZc"
    },

    {
        "title": "Place Value Session 3",
        "topic": "place value",
        "keywords": [
            "place value",
            "number sense",
            "hundreds"
        ],
        "date": "20/06/2020",
        "url": "https://youtu.be/t_tN0s4gnhI"
    },

    {
        "title": "Word Problem Addition 1",
        "topic": "word problem",
        "keywords": [
            "word problem",
            "addition",
            "story sum"
        ],
        "date": "27/06/2020",
        "url": "https://youtu.be/HEgijGQABEw"
    },

    {
        "title": "Word Problem Addition 2",
        "topic": "word problem",
        "keywords": [
            "word problem",
            "addition",
            "problem solving"
        ],
        "date": "27/06/2020",
        "url": "https://youtu.be/B0i-AFqh3l4"
    },

    {
        "title": "Word Problem Add Sub",
        "topic": "word problem",
        "keywords": [
            "addition",
            "subtraction",
            "word problem"
        ],
        "date": "04/07/2020",
        "url": "https://youtu.be/jV5-Pa2C73E"
    },

    {
        "title": "Word Problem Session",
        "topic": "word problem",
        "keywords": [
            "word problem",
            "problem solving"
        ],
        "date": "11/07/2020",
        "url": "https://youtu.be/gOszHLHMgKI"
    },

    {
        "title": "Word Problem Session",
        "topic": "word problem",
        "keywords": [
            "word problem",
            "problem solving"
        ],
        "date": "18/07/2020",
        "url": "https://youtu.be/kERMsSkW6pE"
    },

    {
        "title": "Word Problem Session",
        "topic": "word problem",
        "keywords": [
            "word problem",
            "problem solving"
        ],
        "date": "25/07/2020",
        "url": "https://youtu.be/h5SV_uPpCrA"
    },

    {
        "title": "Word Problem Part 1",
        "topic": "word problem",
        "keywords": [
            "word problem",
            "addition"
        ],
        "date": "08/08/2020",
        "url": "https://youtu.be/qJS0R_xBDvU"
    },

    {
        "title": "Word Problem Part 2",
        "topic": "word problem",
        "keywords": [
            "word problem",
            "addition",
            "subtraction"
        ],
        "date": "08/08/2020",
        "url": "https://youtu.be/f4HbQM3qma8"
    },

    {
        "title": "Word Problem Part 3",
        "topic": "word problem",
        "keywords": [
            "word problem",
            "problem solving"
        ],
        "date": "08/08/2020",
        "url": "https://youtu.be/tCuZMkZ9yds"
    },

    {
        "title": "Math Session",
        "topic": "mathematics",
        "keywords": [
            "mathematics",
            "number sense"
        ],
        "date": "15/08/2020",
        "url": "https://youtu.be/k7dOko_vZEk"
    },

    {
        "title": "Math Session",
        "topic": "mathematics",
        "keywords": [
            "mathematics"
        ],
        "date": "29/08/2020",
        "url": "https://youtu.be/QMBqxF1BHaE"
    },

    {
        "title": "Math Session",
        "topic": "mathematics",
        "keywords": [
            "mathematics"
        ],
        "date": "05/09/2020",
        "url": "https://youtu.be/-F-8pN4MAyM"
    },

    {
        "title": "Math Session",
        "topic": "mathematics",
        "keywords": [
            "mathematics"
        ],
        "date": "12/09/2020",
        "url": "https://youtu.be/nTrfFKgWkYU"
    },

    {
        "title": "Math Session",
        "topic": "mathematics",
        "keywords": [
            "mathematics"
        ],
        "date": "19/09/2020",
        "url": "https://youtu.be/7_BKXGwHijg"
    },

    {
        "title": "Math Session",
        "topic": "mathematics",
        "keywords": [
            "mathematics"
        ],
        "date": "10/10/2020",
        "url": "https://youtu.be/mWylO7CvI-E"
    },

    {
        "title": "Math Session",
        "topic": "mathematics",
        "keywords": [
            "mathematics"
        ],
        "date": "17/10/2020",
        "url": "https://youtu.be/aCVnOvK6YJI"
    },

    {
        "title": "Math Session",
        "topic": "mathematics",
        "keywords": [
            "mathematics"
        ],
        "date": "24/10/2020",
        "url": "https://youtu.be/0SxEwisQnL4"
    }
]

# =====================================================
# YOUTUBE CLIENT
# =====================================================

youtube = build(
    "youtube",
    "v3",
    developerKey=YOUTUBE_API_KEY
)

# =====================================================
# FETCH CHANNEL VIDEOS
# =====================================================

def fetch_channel_videos(channel_id):

    videos = []
    next_page = None

    while True:

        response = youtube.search().list(
            part="snippet",
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page,
            order="date"
        ).execute()

        for item in response.get("items", []):

            if item["id"]["kind"] != "youtube#video":
                continue

            vid = item["id"]["videoId"]

            videos.append(
                Document(
                    page_content=f"""
TITLE: {item['snippet']['title']}

TOPIC:
mathematics

KEYWORDS:
mathematics, teaching strategies, classroom practice

URL:
https://youtu.be/{vid}
""",
                    metadata={
                        "title": item["snippet"]["title"],
                        "url": f"https://youtu.be/{vid}",
                        "source": "youtube_channel"
                    }
                )
            )

        next_page = response.get("nextPageToken")

        if not next_page:
            break

    return videos

# =====================================================
# BUILD DOCUMENTS
# =====================================================

print("Loading embeddings...")
embeddings = get_embeddings()

documents = []

for channel in YOUTUBE_CHANNELS:

    print(f"Fetching channel {channel}")

    documents.extend(
        fetch_channel_videos(channel)
    )

print("Adding Sundaram recordings...")

for v in SUNDRAM_RECORDINGS:

    documents.append(
        Document(
            page_content=f"""
TITLE: {v['title']}

TOPIC:
{v['topic']}

KEYWORDS:
{', '.join(v['keywords'])}

DATE:
{v['date']}

URL:
{v['url']}
""",
            metadata={
                "title": v["title"],
                "topic": v["topic"],
                "url": v["url"],
                "source": "sundaram_recordings"
            }
        )
    )

print(f"Total videos indexed: {len(documents)}")

# =====================================================
# BUILD FAISS
# =====================================================

youtube_db = FAISS.from_documents(
    documents,
    embeddings
)

youtube_db.save_local(
    YOUTUBE_FAISS_PATH
)

print("✅ YouTube FAISS created")
print("📦 Files created:")
print("   index.faiss")
print("   index.pkl")