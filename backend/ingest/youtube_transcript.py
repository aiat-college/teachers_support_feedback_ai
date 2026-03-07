from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    CouldNotRetrieveTranscript
)

def get_transcript_api(video_id: str) -> str | None:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=["en", "en-US", "en-GB"]
        )
        return " ".join(t["text"] for t in transcript)

    except (TranscriptsDisabled, NoTranscriptFound):
        print("⚠️ Transcript not available via API")

    except CouldNotRetrieveTranscript:
        print("⚠️ YouTube blocked transcript API")

    except Exception as e:
        print("⚠️ Transcript API error:", e)

    return None
