import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi


def chunk_text(text: str, chunk_size: int = 2000, overlap: int = 200) -> list[str]:
    if len(text) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + chunk_size])
        start += chunk_size - overlap
    return chunks


def fetch_video_metadata(playlist_url: str) -> list[dict]:
    ydl_opts = {
        "quiet": True,
        "extract_flat": True,
        "skip_download": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
    return [
        {
            "id": entry["id"],
            "title": entry.get("title", ""),
            "url": f"https://youtube.com/watch?v={entry['id']}",
        }
        for entry in info.get("entries", [])
    ]


def fetch_transcript(video_id: str) -> str | None:
    try:
        transcript = YouTubeTranscriptApi().fetch(video_id)
        return " ".join(s.text for s in transcript)
    except Exception:
        return None
