import chromadb
from unittest.mock import patch

import rag


def make_test_collection():
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

    chunk2 = {**chunk, "text": "updated text"}
    rag.upsert_chunks(collection, [chunk2])

    result = collection.get(ids=["vid2_chunk_0"])
    assert result["ids"] == ["vid2_chunk_0"]
