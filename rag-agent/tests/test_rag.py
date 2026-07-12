import uuid
import chromadb
from unittest.mock import patch

import rag


def make_test_collection():
    client = chromadb.EphemeralClient()
    return client.get_or_create_collection(name=f"test_{uuid.uuid4().hex}")


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

    chunk2 = {**chunk, "text": "updated text"}
    rag.upsert_chunks(collection, [chunk2])

    result = collection.get(ids=["vid2_chunk_0"])
    assert result["ids"] == ["vid2_chunk_0"]


def test_query_creator_returns_filtered_results():
    collection = make_test_collection()

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
