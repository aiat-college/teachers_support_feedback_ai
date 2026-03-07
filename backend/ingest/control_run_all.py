"""
Controller to run all ingestion pipelines
"""

from backend.ingest.ingest_pdf import ingest_pdf
from backend.ingest.ingest_youtube import ingest_youtube_channel
from backend.ingest.ingest_websites import ingest_websites


def run_all():
    print("🚀 Starting full ingestion pipeline\n")

    print("📄 Ingesting PDFs...")
    ingest_pdf()

    print("\n▶ Ingesting YouTube...")
    ingest_youtube_channel(
       "https://www.youtube.com/watch?v=RE8IPTTA4-g"
    )

    print("\n🌐 Ingesting Websites...")
    ingest_websites()

    print("\n✅ All ingestion completed successfully!")


if __name__ == "__main__":
    run_all()
