import os
import chromadb
from google import genai
from dotenv import load_dotenv

load_dotenv()

_client: genai.Client | None = None

EMBEDDING_MODEL = "gemini-embedding-001"
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


def query_all(
    collection: chromadb.Collection,
    question: str,
    n_results: int = 5,
) -> list[dict]:
    available = len(collection.get()["ids"])
    if available == 0:
        return []

    query_embedding = embed_text(question, task_type="RETRIEVAL_QUERY")
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, available),
    )

    return [
        {
            "id": results["ids"][0][i],
            "text": results["documents"][0][i],
            "source": results["metadatas"][0][i]["source"],
            "video_id": results["metadatas"][0][i]["video_id"],
            "title": results["metadatas"][0][i]["title"],
            "url": results["metadatas"][0][i]["url"],
            "timestamp": results["metadatas"][0][i].get("timestamp", 0),
        }
        for i in range(len(results["ids"][0]))
    ]


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
                "timestamp": c.get("timestamp", 0),
            }
            for c in chunks
        ],
    )
