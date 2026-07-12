from ingest import chunk_text


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
