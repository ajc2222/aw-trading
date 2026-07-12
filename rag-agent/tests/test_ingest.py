from unittest.mock import patch

from ingest import chunk_text, fetch_video_metadata, fetch_transcript


def test_chunk_text_short_text():
    chunks = chunk_text("hello world", chunk_size=2000, overlap=200)
    assert chunks == ["hello world"]


def test_chunk_text_exact_size():
    text = "a" * 2000
    chunks = chunk_text(text, chunk_size=2000, overlap=200)
    assert chunks == [text]


def test_chunk_text_produces_overlap():
    text = "ab" * 250 + "cd" * 250 + "ef" * 250  # 1500 chars
    chunks = chunk_text(text, chunk_size=500, overlap=100)
    assert len(chunks) >= 2
    assert chunks[0][-100:] == chunks[1][:100]


def test_chunk_text_no_empty_chunks():
    text = "x" * 3000
    chunks = chunk_text(text, chunk_size=2000, overlap=200)
    assert all(len(c) > 0 for c in chunks)


def test_fetch_video_metadata_returns_list():
    mock_info = {
        "entries": [
            {"id": "abc123", "title": "Video One"},
            {"id": "def456", "title": "Video Two"},
        ]
    }
    with patch("yt_dlp.YoutubeDL") as MockYDL:
        instance = MockYDL.return_value.__enter__.return_value
        instance.extract_info.return_value = mock_info
        result = fetch_video_metadata("https://youtube.com/playlist?list=PL123")

    assert result == [
        {"id": "abc123", "title": "Video One", "url": "https://youtube.com/watch?v=abc123"},
        {"id": "def456", "title": "Video Two", "url": "https://youtube.com/watch?v=def456"},
    ]


def test_fetch_video_metadata_empty_playlist():
    mock_info = {"entries": []}
    with patch("yt_dlp.YoutubeDL") as MockYDL:
        instance = MockYDL.return_value.__enter__.return_value
        instance.extract_info.return_value = mock_info
        result = fetch_video_metadata("https://youtube.com/playlist?list=empty")
    assert result == []


def test_fetch_transcript_returns_joined_text():
    from youtube_transcript_api._transcripts import FetchedTranscriptSnippet
    mock_snippets = [
        FetchedTranscriptSnippet(text="Hello there.", start=0.0, duration=1.5),
        FetchedTranscriptSnippet(text="Welcome to trading.", start=1.5, duration=2.0),
    ]
    with patch("ingest.YouTubeTranscriptApi") as MockAPI:
        MockAPI.return_value.fetch.return_value = mock_snippets
        result = fetch_transcript("abc123")
    assert result == "Hello there. Welcome to trading."


def test_fetch_transcript_returns_none_on_error():
    with patch("ingest.YouTubeTranscriptApi") as MockAPI:
        MockAPI.return_value.fetch.side_effect = Exception("no captions")
        result = fetch_transcript("abc123")
    assert result is None


# --- ingest_creator tests ---

import chromadb
from ingest import ingest_creator


def test_ingest_creator_upserts_chunks():
    collection = chromadb.EphemeralClient().get_or_create_collection(f"test_ic_{__import__('uuid').uuid4().hex}")
    creator_config = {"name": "Flux Trades", "playlist_url": "https://youtube.com/playlist?list=PL1"}

    with patch("ingest.fetch_video_metadata") as mock_meta, \
         patch("ingest.fetch_transcript") as mock_tx, \
         patch("rag.embed_text") as mock_embed:

        mock_meta.return_value = [{"id": "v1", "title": "Vid 1", "url": "https://yt.com/v1"}]
        mock_tx.return_value = "a" * 5000
        mock_embed.return_value = [0.1] * 768

        ingest_creator(collection, "flux_trades", creator_config)

    result = collection.get(where={"source": "flux_trades"})
    assert len(result["ids"]) > 0
    assert all(m["video_id"] == "v1" for m in result["metadatas"])


def test_ingest_creator_skips_video_already_indexed():
    collection = chromadb.EphemeralClient().get_or_create_collection(f"test_skip_{__import__('uuid').uuid4().hex}")
    creator_config = {"name": "Flux Trades", "playlist_url": "https://youtube.com/playlist?list=PL1"}

    collection.upsert(
        ids=["v1_chunk_0"],
        embeddings=[[0.0] * 768],
        documents=["existing content"],
        metadatas=[{"source": "flux_trades", "video_id": "v1", "title": "Vid 1", "url": "https://yt.com/v1"}],
    )

    with patch("ingest.fetch_video_metadata") as mock_meta, \
         patch("ingest.fetch_transcript") as mock_tx, \
         patch("rag.embed_text") as mock_embed:

        mock_meta.return_value = [{"id": "v1", "title": "Vid 1", "url": "https://yt.com/v1"}]
        mock_tx.return_value = "new content for v1"
        mock_embed.return_value = [0.9] * 768

        ingest_creator(collection, "flux_trades", creator_config)

    mock_tx.assert_not_called()
