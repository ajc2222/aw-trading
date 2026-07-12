import argparse
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi

import rag
from config import CREATORS


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


def ingest_creator(collection, creator_key: str, creator_config: dict) -> None:
    print(f"Ingesting {creator_config['name']}...")

    existing = collection.get(where={"source": creator_key})
    indexed_video_ids = {m["video_id"] for m in existing["metadatas"]}

    videos = fetch_video_metadata(creator_config["playlist_url"])
    print(f"  Found {len(videos)} videos in playlist")

    for video in videos:
        if video["id"] in indexed_video_ids:
            print(f"  Skipping {video['id']} (already indexed)")
            continue

        transcript = fetch_transcript(video["id"])
        if transcript is None:
            print(f"  Skipping {video['id']} (no transcript)")
            continue

        chunks_text = chunk_text(transcript)
        chunks = [
            {
                "id": f"{video['id']}_chunk_{i}",
                "text": text,
                "embedding": rag.embed_text(text),
                "source": creator_key,
                "video_id": video["id"],
                "title": video["title"],
                "url": video["url"],
            }
            for i, text in enumerate(chunks_text)
        ]
        rag.upsert_chunks(collection, chunks)
        print(f"  Indexed {video['id']} ({len(chunks)} chunks)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest YouTube transcripts into ChromaDB")
    parser.add_argument("--source", help="Creator key to ingest (default: all)", choices=list(CREATORS.keys()))
    args = parser.parse_args()

    collection = rag.get_collection()
    targets = {args.source: CREATORS[args.source]} if args.source else CREATORS

    for key, config in targets.items():
        if not config["playlist_url"]:
            print(f"Skipping {key} — playlist_url not set in config.py")
            continue
        ingest_creator(collection, key, config)

    print("Done.")


if __name__ == "__main__":
    main()
