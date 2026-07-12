from unittest.mock import patch, MagicMock

from bot import build_prompt, generate_answer, format_response, split_message


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

    with patch("bot._get_client") as mock_get_client:
        mock_get_client.return_value.models.generate_content.return_value = mock_response
        result = generate_answer("some prompt")

    assert result == "A fair value gap is an imbalance in price."


def test_format_response_includes_answer():
    result = format_response("FVGs are price imbalances.", SAMPLE_CHUNKS)
    assert "FVGs are price imbalances." in result


def test_format_response_includes_source_titles_and_urls():
    result = format_response("FVGs are price imbalances.", SAMPLE_CHUNKS)
    assert "FVG Explained" in result
    assert "https://youtube.com/watch?v=v1" in result


def test_format_response_deduplicates_sources():
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
