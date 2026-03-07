from backend.ingest.youtube_utils import ingest_youtube_videos

YOUTUBE_URLS = [
    "https://www.youtube.com/watch?v=ZaytG92fB8s&list=PLvLOGBdP8i1_w3346zf9azwTDSEfiJOO4"
]

if __name__ == "__main__":
    support_vectordb = ingest_youtube_videos(YOUTUBE_URLS)
    print("🎉 Total videos ingested:", len(support_vectordb))