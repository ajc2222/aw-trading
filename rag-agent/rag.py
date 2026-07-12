import os
import chromadb
from google import genai
from dotenv import load_dotenv

load_dotenv()

_client: genai.Client | None = None

EMBEDDING_MODEL = "text-embedding-004"
COLLECTION_NAME = "trading_content"


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    return _client


def get_collection(path: str | None = None) -> chromadb.Collection:
    db_path = path or os.getenv("CHROMA_DB_PATH", "./chroma_db")
    client = chromadb.PersistentClient(path=db_path)
    return client.get_or_create_collection(name=COLLECTION_NAME)


def embed_text(text: str, task_type: str = "RETRIEVAL_DOCUMENT") -> list[float]:
    result = _get_client().models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config={"task_type": task_type},
    )
    return result.embeddings[0].values


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
