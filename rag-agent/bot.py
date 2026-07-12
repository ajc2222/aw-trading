import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from google import genai

import rag
from config import CREATORS

load_dotenv()

_client: genai.Client | None = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client


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
    response = _get_client().models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )
    return response.text


def format_response(answer: str, chunks: list[dict]) -> str:
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
