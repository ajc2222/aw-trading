import os
import re
import discord
from dotenv import load_dotenv
from groq import Groq

import rag

load_dotenv()

_client: Groq | None = None


def _get_client() -> Groq:
    global _client
    if _client is None:
        _client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    return _client


def build_prompt(chunks: list[dict], question: str) -> str:
    context = "\n\n".join(f"[{c['title']}]\n{c['text']}" for c in chunks)
    return (
        f"You are a trading assistant answering questions based on content from multiple trading educators. "
        f"Use only the context below to answer. Be concise and specific. If the answer isn't in the context, say so.\n\n"
        f"CONTEXT:\n{context}\n\n"
        f"QUESTION: {question}\n\n"
        f"ANSWER:"
    )


def generate_answer(prompt: str) -> str:
    response = _get_client().chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


def format_response(answer: str, chunks: list[dict]) -> str:
    top = chunks[0]
    ts = top.get("timestamp", 0)
    time_str = f"{ts // 60}:{ts % 60:02d}" if ts else None
    source_line = f"[{top['title']}]({top['url']})"
    if time_str:
        source_line += f" (at {time_str})"
    return f"{answer}\n\n**Source:** {source_line}"


def split_message(text: str, limit: int = 2000) -> list[str]:
    if len(text) <= limit:
        return [text]
    return [text[i : i + limit] for i in range(0, len(text), limit)]


intents = discord.Intents.default()
intents.message_content = True
_discord_client = discord.Client(intents=intents)

_collection = None


@_discord_client.event
async def on_ready() -> None:
    global _collection
    _collection = rag.get_collection()
    print(f"Bot ready as {_discord_client.user}.")


@_discord_client.event
async def on_message(message: discord.Message) -> None:
    if message.author.bot:
        return
    if _discord_client.user not in message.mentions:
        return

    question = re.sub(r"<@!?\d+>", "", message.content).strip()
    if not question:
        await message.reply("Ask me anything about trading — just mention me and type your question.")
        return

    async with message.channel.typing():
        chunks = rag.query_all(_collection, question)
        if not chunks:
            await message.reply("No content indexed yet. Run `python ingest.py` first.")
            return

        try:
            prompt = build_prompt(chunks, question)
            answer = generate_answer(prompt)
            full_response = format_response(answer, chunks)
        except Exception as e:
            await message.reply(f"Error generating answer: {e}")
            return

    for part in split_message(full_response):
        await message.reply(part)


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN not set in .env")
    _discord_client.run(token)
