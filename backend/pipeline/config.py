# backend/config.py

from pathlib import Path

# ===============================
# PROJECT ROOT
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent

# ===============================
# DATA DIRECTORIES
# ===============================
DATA_DIR = BASE_DIR / "data"

PDF_DIR = DATA_DIR / "pdfs"
TXT_DIR = DATA_DIR / "texts"
VECTOR_DB_DIR = DATA_DIR / "vectorstore"

# Create folders if not exist
PDF_DIR.mkdir(parents=True, exist_ok=True)
TXT_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

# ===============================
# INGESTION SETTINGS
# ===============================
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# ===============================
# EMBEDDINGS CONFIG
# ===============================
EMBEDDING_PROVIDER = "ollama"   # "ollama" | "openai"

OLLAMA_EMBED_MODEL = "nomic-embed-text"

# ===============================
# VECTOR DB CONFIG
# ===============================
VECTOR_DB_TYPE = "chroma"
COLLECTION_NAME = "teachers_notes"

# ===============================
# YOUTUBE CONFIG
# ===============================
YOUTUBE_LANGUAGE = "en"

# ===============================
# APP SETTINGS
# ===============================
APP_NAME = "AI Teachers Notes"
APP_VERSION = "0.1.0"
