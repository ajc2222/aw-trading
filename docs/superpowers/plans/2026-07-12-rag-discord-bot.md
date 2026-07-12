# RAG Discord Bot — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local Python RAG system that ingests YouTube trading content from four creators and answers questions via Discord slash commands with per-creator personas powered by Gemini 2.0 Flash.

**Architecture:** Single ChromaDB collection stores chunked transcripts with `source` metadata per creator. `ingest.py` pulls transcripts via `youtube-transcript-api` + `yt-dlp` and upserts Gemini embeddings. `bot.py` registers four slash commands that filter by creator, retrieve top-5 chunks, and generate answers via Gemini 2.0 Flash.

**Tech Stack:** Python 3.11+, chromadb, google-generativeai, discord.py 2.x, youtube-transcript-api, yt-dlp, python-dotenv, pytest

---

## File Map

| File | Responsibility |
|---|---|
| `rag-agent/config.py` | Creator definitions: keys, display names, playlist URLs |
| `rag-agent/rag.py` | ChromaDB client, Gemini embedding, upsert, retrieval query |
| `rag-agent/ingest.py` | YouTube fetch, text chunking, ingestion pipeline, CLI |
| `rag-agent/bot.py` | Discord bot, slash commands, prompt building, Gemini generation, response formatting |
| `rag-agent/requirements.txt` | Python dependencies |
| `rag-agent/.env.example` | Environment variable template |
| `rag-agent/.gitignore` | Ignore chroma_db/ and .env |
| `rag-agent/tests/__init__.py` | Empty package marker |
| `rag-agent/tests/test_rag.py` | Tests for rag.py (chunk, embed, upsert, query) |
| `rag-agent/tests/test_ingest.py` | Tests for ingest.py (fetch mocks, pipeline, dedup) |
| `rag-agent/tests/test_bot.py` | Tests for bot.py (prompt building, formatting, splitting) |

---

### Task 1: Project Scaffold

**Files:**
- Create: `rag-agent/requirements.txt`
- Create: `rag-agent/.env.example`
- Create: `rag-agent/.gitignore`
- Create: `rag-agent/config.py`
- Create: `rag-agent/tests/__init__.py`

- [ ] **Step 1: Create the rag-agent directory and requirements.txt**

```
rag-agent/requirements.txt
```

```
discord.py>=2.3.0
chromadb>=0.5.0
google-generativeai>=0.7.0
youtube-transcript-api>=0.6.0
yt-dlp>=2024.1.0
python-dotenv>=1.0.0
pytest>=8.0.0
```

- [ ] **Step 2: Create .env.example**

```
rag-agent/.env.example
```

```
DISCORD_TOKEN=your_discord_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
CHROMA_DB_PATH=./chroma_db
```

- [ ] **Step 3: Create .gitignore**

```
rag-agent/.gitignore
```

```
.env
chroma_db/
__pycache__/
*.pyc
.pytest_cache/
```

- [ ] **Step 4: Create config.py**

```python
# rag-agent/config.py

CREATORS = {
    "flux_trades": {
        "name": "Flux Trades",
        "playlist_url": "",  # fill in before running ingest
    },
    "aidenomics": {
        "name": "Aidenomics",
        "playlist_url": "",
    },
    "bionic_nq": {
        "name": "BionicNQ",
        "playlist_url": "",
    },
    "gxt": {
        "name": "GXT",
        "playlist_url": "",
    },
}
```

- [ ] **Step 5: Create tests/__init__.py**

Empty file — just `touch rag-agent/tests/__init__.py`

- [ ] **Step 6: Install dependencies**

```bash
cd rag-agent
pip install -r requirements.txt
```

Expected: all packages install without error.

- [ ] **Step 7: Commit**

```bash
git add rag-agent/
git commit -m "feat: scaffold rag-agent project structure"
```

---

### Task 2: Text Chunking

**Files:**
- Create: `rag-agent/ingest.py` (chunk_text only)
- Create: `rag-agent/tests/test_ingest.py`

- [ ] **Step 1: Write the failing tests**

```python
# rag-agent/tests/test_ingest.py

from ingest import chunk_text


def test_chunk_text_short_text():
    # Text shorter than chunk_size returns as single chunk
    chunks = chunk_text("hello world", chunk_size=2000, overlap=200)
    assert chunks == ["hello world"]


def test_chunk_text_exact_size():
    text = "a" * 2000
    chunks = chunk_text(text, chunk_size=2000, overlap=200)
    assert chunks == [text]


def test_chunk_text_produces_overlap():
    # chunk 0 ends at 500, chunk 1 starts at 400 — overlapping 100 chars
    text = "ab" * 250 + "cd" * 250 + "ef" * 250  # 1500 chars
    chunks = chunk_text(text, chunk_size=500, overlap=100)
    assert len(chunks) >= 2
    # The last 100 chars of chunk[0] == first 100 chars of chunk[1]
    assert chunks[0][-100:] == chunks[1][:100]


def test_chunk_text_no_empty_chunks():
    text = "x" * 3000
    chunks = chunk_text(text, chunk_size=2000, overlap=200)
    assert all(len(c) > 0 for c in chunks)
```

- [ ] **Step 2: Run to confirm failure**

```bash
cd rag-agent
pytest tests/test_ingest.py -v
```

Expected: `ImportError: cannot import name 'chunk_text' from 'ingest'`

- [ ] **Step 3: Implement chunk_text in ingest.py**

```python
# rag-agent/ingest.py


def chunk_text(text: str, chunk_size: int = 2000, overlap: int = 200) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start : start + chunk_size])
        start += chunk_size - overlap
    return chunks
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
pytest tests/test_ingest.py -v
```

Expected: 4 PASSED

- [ ] **Step 5: Commit**

```bash
git add rag-agent/ingest.py rag-agent/tests/test_ingest.py
git commit -m "feat: add chunk_text with overlap"
```

---

### Task 3: ChromaDB Setup, Embedding, and Upsert

**Files:**
- Create: `rag-agent/rag.py`
- Create: `rag-agent/tests/test_rag.py`

- [ ] **Step 1: Write failing tests**

```python
# rag-agent/tests/test_rag.py

import chromadb
import pytest
from unittest.mock import patch, MagicMock

import rag


def make_test_collection():
    """Ephemeral in-memory ChromaDB collection for tests."""
    client = chromadb.EphemeralClient()
    return client.get_or_create_collection(name="test_collection")


def test_upsert_chunks_stores_documents():
    collection = make_test_collection()
    chunks = [
        {
            "id": "vid1_chunk_0",
            "text": "ICT concepts explained",
            "embedding": [0.1] * 768,
            "source": "flux_trades",
            "video_id": "vid1",
            "title": "ICT Tutorial",
            "url": "https://youtube.com/watch?v=vid1",
        }
    ]

    rag.upsert_chunks(collection, chunks)

    result = collection.get(ids=["vid1_chunk_0"])
    assert result["ids"] == ["vid1_chunk_0"]
    assert result["documents"] == ["ICT concepts explained"]
    assert result["metadatas"][0]["source"] == "flux_trades"
    assert result["metadatas"][0]["video_id"] == "vid1"


def test_upsert_chunks_skips_existing_video():
    collection = make_test_collection()
    chunk = {
        "id": "vid2_chunk_0",
        "text": "original text",
        "embedding": [0.2] * 768,
        "source": "aidenomics",
        "video_id": "vid2",
        "title": "Some Video",
        "url": "https://youtube.com/watch?v=vid2",
    }

    rag.upsert_chunks(collection, [chunk])

    # Second upsert with same id — ChromaDB upsert is idempotent
    chunk2 = {**chunk, "text": "updated text"}
    rag.upsert_chunks(collection, [chunk2])

    result = collection.get(ids=["vid2_chunk_0"])
    # upsert overwrites — we verify the call succeeds without error
    assert result["ids"] == ["vid2_chunk_0"]
```

- [ ] **Step 2: Run to confirm failure**

```bash
cd rag-agent
pytest tests/test_rag.py -v
```

Expected: `ImportError: No module named 'rag'`

- [ ] **Step 3: Implement rag.py with ChromaDB setup, embed_text, and upsert_chunks**

```python
# rag-agent/rag.py

import os
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

EMBEDDING_MODEL = "models/text-embedding-004"
COLLECTION_NAME = "trading_content"


def get_collection(path: str | None = None) -> chromadb.Collection:
    db_path = path or os.getenv("CHROMA_DB_PATH", "./chroma_db")
    client = chromadb.PersistentClient(path=db_path)
    return client.get_or_create_collection(name=COLLECTION_NAME)


def embed_text(text: str, task_type: str = "retrieval_document") -> list[float]:
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type=task_type,
    )
    return result["embedding"]


def upsert_chunks(collection: chromadb.Collection, chunks: list[dict]) -> None:
    if not chunks:
        return
    collection.upsert(
        ids=[c["id"] for c in chunks],
        embeddings=[c["embedding"] for c in chunks],
        documents=[c["text"] for c in chunks],
        metadatas=[
            {
                "source": c["source"],
                "video_id": c["video_id"],
                "title": c["title"],
                "url": c["url"],
            }
            for c in chunks
        ],
    )
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
pytest tests/test_rag.py -v
```

Expected: 2 PASSED

- [ ] **Step 5: Commit**

```bash
git add rag-agent/rag.py rag-agent/tests/test_rag.py
git commit -m "feat: add ChromaDB setup, embedding, and upsert"
```

---

### Task 4: Retrieval Query

**Files:**
- Modify: `rag-agent/rag.py` (add query_creator)
- Modify: `rag-agent/tests/test_rag.py` (add query tests)

- [ ] **Step 1: Write failing tests**

Add these tests to `rag-agent/tests/test_rag.py`:

```python
def test_query_creator_returns_filtered_results():
    collection = make_test_collection()

    # Insert two chunks from different creators
    collection.upsert(
        ids=["ft_chunk_0", "ai_chunk_0"],
        embeddings=[[0.1] * 768, [0.1] * 768],
        documents=["flux trades content", "aidenomics content"],
        metadatas=[
            {"source": "flux_trades", "video_id": "v1", "title": "FT Video", "url": "https://yt.com/v1"},
            {"source": "aidenomics", "video_id": "v2", "title": "AI Video", "url": "https://yt.com/v2"},
        ],
    )

    with patch("rag.embed_text", return_value=[0.1] * 768):
        results = rag.query_creator(collection, source="flux_trades", question="what is ICT?", n_results=5)

    assert len(results) == 1
    assert results[0]["source"] == "flux_trades"
    assert results[0]["text"] == "flux trades content"
    assert results[0]["title"] == "FT Video"
    assert results[0]["url"] == "https://yt.com/v1"


def test_query_creator_empty_collection_returns_empty():
    collection = make_test_collection()
    with patch("rag.embed_text", return_value=[0.1] * 768):
        results = rag.query_creator(collection, source="flux_trades", question="test", n_results=5)
    assert results == []
```

- [ ] **Step 2: Run to confirm failure**

```bash
pytest tests/test_rag.py::test_query_creator_returns_filtered_results -v
```

Expected: `AttributeError: module 'rag' has no attribute 'query_creator'`

- [ ] **Step 3: Add query_creator to rag.py**

Append to `rag-agent/rag.py`:

```python
def query_creator(
    collection: chromadb.Collection,
    source: str,
    question: str,
    n_results: int = 5,
) -> list[dict]:
    query_embedding = embed_text(question, task_type="retrieval_query")

    # Count docs for this source so we don't request more than exist
    existing = collection.get(where={"source": source})
    available = len(existing["ids"])
    if available == 0:
        return []

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, available),
        where={"source": source},
    )

    chunks = []
    for i, doc_id in enumerate(results["ids"][0]):
        meta = results["metadatas"][0][i]
        chunks.append(
            {
                "id": doc_id,
                "text": results["documents"][0][i],
                "source": meta["source"],
                "video_id": meta["video_id"],
                "title": meta["title"],
                "url": meta["url"],
            }
        )
    return chunks
```

- [ ] **Step 4: Run all rag tests**

```bash
pytest tests/test_rag.py -v
```

Expected: 4 PASSED

- [ ] **Step 5: Commit**

```bash
git add rag-agent/rag.py rag-agent/tests/test_rag.py
git commit -m "feat: add query_creator with source filtering"
```

---

### Task 5: YouTube Transcript Fetching

**Files:**
- Modify: `rag-agent/ingest.py` (add fetch functions)
- Modify: `rag-agent/tests/test_ingest.py` (add fetch tests)

- [ ] **Step 1: Write failing tests**

Add to `rag-agent/tests/test_ingest.py`:

```python
from unittest.mock import patch, MagicMock

from ingest import fetch_video_metadata, fetch_transcript


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
    mock_transcript = [
        {"text": "Hello there.", "start": 0.0, "duration": 1.5},
        {"text": "Welcome to trading.", "start": 1.5, "duration": 2.0},
    ]
    with patch("youtube_transcript_api.YouTubeTranscriptApi.get_transcript", return_value=mock_transcript):
        result = fetch_transcript("abc123")
    assert result == "Hello there. Welcome to trading."


def test_fetch_transcript_returns_none_on_error():
    with patch("youtube_transcript_api.YouTubeTranscriptApi.get_transcript", side_effect=Exception("no captions")):
        result = fetch_transcript("abc123")
    assert result is None
```

- [ ] **Step 2: Run to confirm failure**

```bash
pytest tests/test_ingest.py::test_fetch_video_metadata_returns_list -v
```

Expected: `ImportError: cannot import name 'fetch_video_metadata' from 'ingest'`

- [ ] **Step 3: Add fetch functions to ingest.py**

Append to `rag-agent/ingest.py`:

```python
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi


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
        segments = YouTubeTranscriptApi.get_transcript(video_id)
        return " ".join(s["text"] for s in segments)
    except Exception:
        return None
```

- [ ] **Step 4: Run all ingest tests**

```bash
pytest tests/test_ingest.py -v
```

Expected: 8 PASSED

- [ ] **Step 5: Commit**

```bash
git add rag-agent/ingest.py rag-agent/tests/test_ingest.py
git commit -m "feat: add YouTube transcript and metadata fetching"
```

---

### Task 6: Ingestion Pipeline + CLI

**Files:**
- Modify: `rag-agent/ingest.py` (add ingest_creator, main)
- Modify: `rag-agent/tests/test_ingest.py` (add pipeline tests)

- [ ] **Step 1: Write failing tests**

Add to `rag-agent/tests/test_ingest.py`:

```python
import chromadb
from ingest import ingest_creator


def test_ingest_creator_upserts_chunks():
    collection = chromadb.EphemeralClient().get_or_create_collection("test")
    creator_config = {"name": "Flux Trades", "playlist_url": "https://youtube.com/playlist?list=PL1"}

    with patch("ingest.fetch_video_metadata") as mock_meta, \
         patch("ingest.fetch_transcript") as mock_tx, \
         patch("rag.embed_text") as mock_embed:

        mock_meta.return_value = [{"id": "v1", "title": "Vid 1", "url": "https://yt.com/v1"}]
        mock_tx.return_value = "a" * 5000  # long enough to produce multiple chunks
        mock_embed.return_value = [0.1] * 768

        ingest_creator(collection, "flux_trades", creator_config)

    result = collection.get(where={"source": "flux_trades"})
    assert len(result["ids"]) > 0
    assert all(m["video_id"] == "v1" for m in result["metadatas"])


def test_ingest_creator_skips_video_already_indexed():
    collection = chromadb.EphemeralClient().get_or_create_collection("test")
    creator_config = {"name": "Flux Trades", "playlist_url": "https://youtube.com/playlist?list=PL1"}

    # Pre-populate with a sentinel chunk for v1
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

    # fetch_transcript should not have been called since v1 is already indexed
    mock_tx.assert_not_called()
```

- [ ] **Step 2: Run to confirm failure**

```bash
pytest tests/test_ingest.py::test_ingest_creator_upserts_chunks -v
```

Expected: `ImportError: cannot import name 'ingest_creator' from 'ingest'`

- [ ] **Step 3: Add ingest_creator and main to ingest.py**

Add these imports at the top of `rag-agent/ingest.py`:

```python
import argparse
import rag
from config import CREATORS
```

Then append:

```python
def ingest_creator(collection, creator_key: str, creator_config: dict) -> None:
    print(f"Ingesting {creator_config['name']}...")

    # Collect already-indexed video IDs for dedup
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
```

- [ ] **Step 4: Run all ingest tests**

```bash
pytest tests/test_ingest.py -v
```

Expected: 10 PASSED

- [ ] **Step 5: Commit**

```bash
git add rag-agent/ingest.py rag-agent/tests/test_ingest.py
git commit -m "feat: add ingestion pipeline with dedup and CLI"
```

---

### Task 7: Prompt Building and Answer Generation

**Files:**
- Create: `rag-agent/bot.py` (build_prompt, generate_answer)
- Create: `rag-agent/tests/test_bot.py`

- [ ] **Step 1: Write failing tests**

```python
# rag-agent/tests/test_bot.py

from unittest.mock import patch, MagicMock

from bot import build_prompt, generate_answer


SAMPLE_CHUNKS = [
    {
        "id": "v1_chunk_0",
        "text": "Fair value gaps form when price moves quickly through an area.",
        "source": "flux_trades",
        "video_id": "v1",
        "title": "FVG Explained",
        "url": "https://youtube.com/watch?v=v1",
    },
    {
        "id": "v1_chunk_1",
        "text": "You enter on the retracement back into the FVG.",
        "source": "flux_trades",
        "video_id": "v1",
        "title": "FVG Explained",
        "url": "https://youtube.com/watch?v=v1",
    },
]


def test_build_prompt_contains_creator_name():
    prompt = build_prompt("Flux Trades", SAMPLE_CHUNKS, "What is a fair value gap?")
    assert "Flux Trades" in prompt


def test_build_prompt_contains_question():
    prompt = build_prompt("Flux Trades", SAMPLE_CHUNKS, "What is a fair value gap?")
    assert "What is a fair value gap?" in prompt


def test_build_prompt_contains_chunk_text():
    prompt = build_prompt("Flux Trades", SAMPLE_CHUNKS, "What is a fair value gap?")
    assert "Fair value gaps form when price moves quickly" in prompt
    assert "You enter on the retracement" in prompt


def test_generate_answer_returns_text():
    mock_response = MagicMock()
    mock_response.text = "A fair value gap is an imbalance in price."

    with patch("bot.model") as mock_model:
        mock_model.generate_content.return_value = mock_response
        result = generate_answer("some prompt")

    assert result == "A fair value gap is an imbalance in price."
    mock_model.generate_content.assert_called_once_with("some prompt")
```

- [ ] **Step 2: Run to confirm failure**

```bash
pytest tests/test_bot.py -v
```

Expected: `ImportError: cannot import name 'build_prompt' from 'bot'`

- [ ] **Step 3: Create bot.py with prompt and generation logic**

```python
# rag-agent/bot.py

import os
import discord
from discord import app_commands
from dotenv import load_dotenv
import google.generativeai as genai

import rag
from config import CREATORS

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")


def build_prompt(creator_name: str, chunks: list[dict], question: str) -> str:
    context = "\n\n".join(f"[{c['title']}]\n{c['text']}" for c in chunks)
    return (
        f"You are answering questions based on the trading content of {creator_name}. "
        f"Use only the context below to answer. If the answer isn't in the context, say so.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {question}\n\n"
        f"ANSWER:"
    )


def generate_answer(prompt: str) -> str:
    response = model.generate_content(prompt)
    return response.text
```

- [ ] **Step 4: Run tests to confirm they pass**

```bash
pytest tests/test_bot.py::test_build_prompt_contains_creator_name \
       tests/test_bot.py::test_build_prompt_contains_question \
       tests/test_bot.py::test_build_prompt_contains_chunk_text \
       tests/test_bot.py::test_generate_answer_returns_text -v
```

Expected: 4 PASSED

- [ ] **Step 5: Commit**

```bash
git add rag-agent/bot.py rag-agent/tests/test_bot.py
git commit -m "feat: add prompt building and Gemini answer generation"
```

---

### Task 8: Response Formatting and Message Splitting

**Files:**
- Modify: `rag-agent/bot.py` (add format_response, split_message)
- Modify: `rag-agent/tests/test_bot.py` (add formatting tests)

- [ ] **Step 1: Write failing tests**

Add to `rag-agent/tests/test_bot.py`:

```python
from bot import format_response, split_message


def test_format_response_includes_answer():
    result = format_response("FVGs are price imbalances.", SAMPLE_CHUNKS)
    assert "FVGs are price imbalances." in result


def test_format_response_includes_source_titles_and_urls():
    result = format_response("FVGs are price imbalances.", SAMPLE_CHUNKS)
    assert "FVG Explained" in result
    assert "https://youtube.com/watch?v=v1" in result


def test_format_response_deduplicates_sources():
    # SAMPLE_CHUNKS has two chunks from the same video — source should appear once
    result = format_response("answer", SAMPLE_CHUNKS)
    assert result.count("FVG Explained") == 1


def test_split_message_short_message():
    result = split_message("hello", limit=2000)
    assert result == ["hello"]


def test_split_message_long_message():
    text = "x" * 4500
    parts = split_message(text, limit=2000)
    assert len(parts) == 3
    assert all(len(p) <= 2000 for p in parts)
    assert "".join(parts) == text


def test_split_message_empty():
    result = split_message("", limit=2000)
    assert result == [""]
```

- [ ] **Step 2: Run to confirm failure**

```bash
pytest tests/test_bot.py::test_format_response_includes_answer -v
```

Expected: `ImportError: cannot import name 'format_response' from 'bot'`

- [ ] **Step 3: Add format_response and split_message to bot.py**

Append to `rag-agent/bot.py`:

```python
def format_response(answer: str, chunks: list[dict]) -> str:
    # Deduplicate sources by video_id
    seen = set()
    sources = []
    for chunk in chunks:
        if chunk["video_id"] not in seen:
            seen.add(chunk["video_id"])
            sources.append(f"- [{chunk['title']}]({chunk['url']})")

    source_block = "\n".join(sources)
    return f"{answer}\n\n**Sources:**\n{source_block}"


def split_message(text: str, limit: int = 2000) -> list[str]:
    if len(text) <= limit:
        return [text]
    return [text[i : i + limit] for i in range(0, len(text), limit)]
```

- [ ] **Step 4: Run all bot tests**

```bash
pytest tests/test_bot.py -v
```

Expected: 10 PASSED

- [ ] **Step 5: Commit**

```bash
git add rag-agent/bot.py rag-agent/tests/test_bot.py
git commit -m "feat: add response formatting and message splitting"
```

---

### Task 9: Discord Bot Slash Commands

**Files:**
- Modify: `rag-agent/bot.py` (add Discord client, slash commands, on_ready, run)

No unit tests — Discord interaction requires live connection. Manual test instructions below.

- [ ] **Step 1: Add Discord bot wiring to bot.py**

Append to `rag-agent/bot.py`:

```python
# --- Discord Bot ---

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

collection = None  # initialized in on_ready


async def handle_ask(interaction: discord.Interaction, creator_key: str, question: str) -> None:
    await interaction.response.defer()
    creator = CREATORS[creator_key]
    chunks = rag.query_creator(collection, source=creator_key, question=question)

    if not chunks:
        await interaction.followup.send(
            f"No content indexed for {creator['name']} yet. Run `python ingest.py --source {creator_key}` first."
        )
        return

    prompt = build_prompt(creator["name"], chunks, question)
    answer = generate_answer(prompt)
    full_response = format_response(answer, chunks)

    for part in split_message(full_response):
        await interaction.followup.send(part)


@tree.command(name="ask-fluxtrades", description="Ask a question based on Flux Trades content")
async def ask_fluxtrades(interaction: discord.Interaction, question: str) -> None:
    await handle_ask(interaction, "flux_trades", question)


@tree.command(name="ask-aidenomics", description="Ask a question based on Aidenomics content")
async def ask_aidenomics(interaction: discord.Interaction, question: str) -> None:
    await handle_ask(interaction, "aidenomics", question)


@tree.command(name="ask-bionicnq", description="Ask a question based on BionicNQ content")
async def ask_bionicnq(interaction: discord.Interaction, question: str) -> None:
    await handle_ask(interaction, "bionic_nq", question)


@tree.command(name="ask-gxt", description="Ask a question based on GXT content")
async def ask_gxt(interaction: discord.Interaction, question: str) -> None:
    await handle_ask(interaction, "gxt", question)


@client.event
async def on_ready() -> None:
    global collection
    collection = rag.get_collection()
    await tree.sync()
    print(f"Bot ready as {client.user}. Commands synced.")


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN not set in .env")
    client.run(token)
```

- [ ] **Step 2: Set up environment variables**

Copy `.env.example` to `.env` and fill in values:

```bash
cp rag-agent/.env.example rag-agent/.env
```

Edit `rag-agent/.env`:
```
DISCORD_TOKEN=<your bot token from discord.com/developers/applications>
GEMINI_API_KEY=<your key from aistudio.google.com>
CHROMA_DB_PATH=./chroma_db
```

- [ ] **Step 3: Fill in playlist URLs in config.py**

Edit `rag-agent/config.py` and add the playlist URLs for each creator. YouTube playlist URL format: `https://www.youtube.com/playlist?list=<PLAYLIST_ID>`

You can also use a channel's "Videos" tab URL: `https://www.youtube.com/c/<ChannelName>/videos`

- [ ] **Step 4: Run ingestion for one creator to test the pipeline**

```bash
cd rag-agent
python ingest.py --source flux_trades
```

Expected output:
```
Ingesting Flux Trades...
  Found N videos in playlist
  Indexed <video_id> (K chunks)
  ...
Done.
```

- [ ] **Step 5: Start the bot**

```bash
cd rag-agent
python bot.py
```

Expected output:
```
Bot ready as <YourBotName>#1234. Commands synced.
```

- [ ] **Step 6: Test in Discord**

In your Discord server, type:
```
/ask-fluxtrades What is a fair value gap?
```

Expected: Bot responds with an answer drawn from transcript content + sources footer.

> **Note on slash command sync:** `tree.sync()` with no guild argument does a global sync, which can take up to 1 hour to appear. For instant testing during dev, replace `await tree.sync()` with `await tree.sync(guild=discord.Object(id=YOUR_GUILD_ID))` where `YOUR_GUILD_ID` is your server's ID (right-click server → Copy Server ID). Revert to global sync before sharing with others.

- [ ] **Step 7: Run ingest for remaining creators**

```bash
python ingest.py --source aidenomics
python ingest.py --source bionic_nq
python ingest.py --source gxt
```

- [ ] **Step 8: Commit**

```bash
git add rag-agent/bot.py rag-agent/config.py
git commit -m "feat: add Discord slash commands and wire up full RAG pipeline"
```

---

## Running the System

**One-time setup:**
```bash
cd rag-agent
pip install -r requirements.txt
cp .env.example .env   # fill in tokens
# fill in playlist_url values in config.py
python ingest.py       # ingest all creators
```

**Daily use:**
```bash
python ingest.py       # re-run to pick up new videos (skips already-indexed)
python bot.py          # keep running for Discord
```
