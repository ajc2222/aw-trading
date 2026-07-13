import argparse
import os
import tempfile
import time
import yt_dlp
import whisper
from youtube_transcript_api import YouTubeTranscriptApi

import rag
from config import CREATORS

_whisper_model = None


def _get_whisper_model():
    global _whisper_model
    if _whisper_model is None:
        print("  Loading Whisper model (first time only)...")
        _whisper_model = whisper.load_model("base")
    return _whisper_model


def chunk_segments(segments: list[dict], chunk_size: int = 2000, overlap: int = 200) -> list[tuple[str, int]]:
    """Returns list of (text, start_seconds) for each chunk."""
    full_text = ""
    positions = []  # (char_position, start_seconds)
    for seg in segments:
        positions.append((len(full_text), int(seg["start"])))
        full_text += seg["text"] + " "

    if len(full_text) <= chunk_size:
        return [(full_text, positions[0][1] if positions else 0)]

    chunks = []
    start = 0
    while start < len(full_text):
        chunk_text = full_text[start : start + chunk_size]
        ts = 0
        for pos, t in positions:
            if pos <= start:
                ts = t
            else:
                break
        chunks.append((chunk_text, ts))
        start += chunk_size - overlap
    return chunks


def fetch_video_metadata(playlist_url: str) -> list[dict]:
    ydl_opts = {"quiet": True, "extract_flat": True, "skip_download": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
    return [
        {
            "id": entry["id"],
            "title": entry.get("title", ""),
            "url": f"https://youtube.com/watch?v={entry['id']}",
        }
        for entry in info.get("entries", [])
        if len(entry.get("id", "")) == 11  # skip channel IDs
    ]


def fetch_transcript(video_id: str) -> list[dict] | None:
    # Try YouTube captions first
    try:
        segments = YouTubeTranscriptApi().fetch(video_id)
        return [{"text": s.text, "start": s.start} for s in segments]
    except Exception:
        pass

    # Fall back to Whisper
    audio_path = os.path.join(tempfile.gettempdir(), f"{video_id}.mp3")
    try:
        print(f"    No captions — transcribing with Whisper...")
        ydl_opts = {
            "quiet": True,
            "format": "bestaudio/best",
            "outtmpl": os.path.join(tempfile.gettempdir(), f"{video_id}.%(ext)s"),
            "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "64"}],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([f"https://youtube.com/watch?v={video_id}"])

        result = _get_whisper_model().transcribe(audio_path, fp16=False)
        return [{"text": seg["text"], "start": seg["start"]} for seg in result["segments"]]
    except Exception as e:
        print(f"    Whisper failed: {e}")
        return None
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)


def delete_creator(collection, creator_key: str) -> None:
    existing = collection.get(where={"source": creator_key})
    if existing["ids"]:
        collection.delete(ids=existing["ids"])
        print(f"  Deleted {len(existing['ids'])} chunks for {creator_key}")


def ingest_creator(collection, creator_key: str, creator_config: dict, force: bool = False) -> None:
    print(f"Ingesting {creator_config['name']}...")

    if force:
        delete_creator(collection, creator_key)

    existing = collection.get(where={"source": creator_key})
    indexed_video_ids = {m["video_id"] for m in existing["metadatas"]}

    videos = fetch_video_metadata(creator_config["playlist_url"])
    print(f"  Found {len(videos)} videos in playlist")

    for video in videos:
        if video["id"] in indexed_video_ids:
            print(f"  Skipping {video['id']} (already indexed)")
            continue

        segments = fetch_transcript(video["id"])
        if segments is None:
            print(f"  Skipping {video['id']} (no transcript)")
            continue

        chunks = []
        for i, (text, ts) in enumerate(chunk_segments(segments)):
            chunks.append({
                "id": f"{video['id']}_chunk_{i}",
                "text": text,
                "embedding": rag.embed_text(text),
                "source": creator_key,
                "video_id": video["id"],
                "title": video["title"],
                "url": f"{video['url']}&t={ts}",
                "timestamp": ts,
            })
            time.sleep(0.7)
        rag.upsert_chunks(collection, chunks)
        print(f"  Indexed {video['id']} ({len(chunks)} chunks)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest YouTube transcripts into ChromaDB")
    parser.add_argument("--source", help="Creator key to ingest (default: all)", choices=list(CREATORS.keys()))
    parser.add_argument("--force", action="store_true", help="Delete existing entries before re-ingesting")
    args = parser.parse_args()

    collection = rag.get_collection()
    targets = {args.source: CREATORS[args.source]} if args.source else CREATORS

    for key, config in targets.items():
        if not config.get("playlist_url"):
            print(f"Skipping {key} — playlist_url not set in config.py")
            continue
        ingest_creator(collection, key, config, force=args.force)

    print("Done.")


if __name__ == "__main__":
    main()
