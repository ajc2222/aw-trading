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


# --- Discord Bot ---

intents = discord.Intents.default()
_discord_client = discord.Client(intents=intents)
tree = app_commands.CommandTree(_discord_client)

_collection = None  # initialized in on_ready


async def handle_ask(interaction: discord.Interaction, creator_key: str, question: str) -> None:
    await interaction.response.defer()
    creator = CREATORS[creator_key]
    chunks = rag.query_creator(_collection, source=creator_key, question=question)

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


@_discord_client.event
async def on_ready() -> None:
    global _collection
    _collection = rag.get_collection()
    await tree.sync()
    print(f"Bot ready as {_discord_client.user}. Commands synced.")


if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise RuntimeError("DISCORD_TOKEN not set in .env")
    _discord_client.run(token)
