from backend.ingest.youtube_loader import ingest_youtube

def ingest_youtube_videos(urls):
    texts = []

    for url in urls:
        try:
            text = ingest_youtube(url)
            if text:
                texts.append(text)
                print(f"✅ Ingested: {url}")
            else:
                print(f"⚠️ No transcript: {url}")
        except Exception as e:
            print(f"❌ Failed {url}: {e}")

    return texts
