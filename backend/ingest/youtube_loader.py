from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
from urllib.parse import urlparse, parse_qs


def extract_video_id(youtube_url: str) -> str | None:
    parsed = urlparse(youtube_url)

    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        return parse_qs(parsed.query).get("v", [None])[0]

    if parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")

    return None


def ingest_youtube(youtube_url: str) -> str | None:
    try:
        video_id = extract_video_id(youtube_url)
        if not video_id:
            print(f"❌ Invalid YouTube URL: {youtube_url}")
            return None

        api = YouTubeTranscriptApi()

        # ✅ fetch() returns objects
        transcript = api.fetch(video_id)

        # ✅ FIX IS HERE
        return " ".join(item.text for item in transcript)

    except (TranscriptsDisabled, NoTranscriptFound):
        print(f"⚠️ Transcript not available: {youtube_url}")
        return None
    except Exception as e:
        print(f"❌ Error fetching transcript for {youtube_url}: {e}")
        return None
