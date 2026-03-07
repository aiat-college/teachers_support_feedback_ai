import whisper
import tempfile
import os
import yt_dlp

def get_transcript_whisper(video_url: str) -> str | None:
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            audio_path = os.path.join(tmpdir, "audio.wav")

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": audio_path,
                "quiet": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "wav",
                }]
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])

            model = whisper.load_model("base")
            result = model.transcribe(audio_path)

            return result["text"]

    except Exception as e:
        print("❌ Whisper transcription failed:", e)
        return None
