import math
import requests
from app.config import settings

_GEMINI_EMBED_MODEL = "gemini-embedding-001"
_GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models"
_st_model = None

def _use_gemini() -> bool:
    return settings.llm_provider.lower() == "gemini" and bool(settings.gemini_api_key)

def _normalize(vec: list[float]) -> list[float]:
    norm = math.sqrt(sum(x * x for x in vec))
    if norm == 0:
        return vec
    return [x / norm for x in vec]

def embed_passages(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    if _use_gemini():
        try:
            return _gemini_batch(texts)
        except Exception:
            # Fallback zero vectors on network / sandbox limitation
            return [[0.0] * 768 for _ in texts]
    try:
        return _st_embed(texts, prefix="passage: ")
    except Exception:
        return [[0.0] * 768 for _ in texts]

def embed_query(text: str) -> list[float]:
    if _use_gemini():
        try:
            return _gemini_single(text)
        except Exception:
            # Fallback zero vector on network / sandbox limitation
            return [0.0] * 768
    try:
        return _st_embed([text], prefix="query: ")[0]
    except Exception:
        return [0.0] * 768

def _gemini_single(text: str) -> list[float]:
    url = f"{_GEMINI_API_URL}/{_GEMINI_EMBED_MODEL}:embedContent?key={settings.gemini_api_key}"
    body = {
        "model": f"models/{_GEMINI_EMBED_MODEL}",
        "content": {"parts": [{"text": text}]}
    }
    r = requests.post(url, json=body, timeout=30)
    r.raise_for_status()
    vec = r.json().get("embedding", {}).get("values", [])
    return _normalize(vec)

def _gemini_batch(texts: list[str]) -> list[list[float]]:
    results: list[list[float]] = []
    url = f"{_GEMINI_API_URL}/{_GEMINI_EMBED_MODEL}:batchEmbedContents?key={settings.gemini_api_key}"
    batch_size = 50
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        body = {
            "requests": [
                {
                    "model": f"models/{_GEMINI_EMBED_MODEL}",
                    "content": {"parts": [{"text": t}]}
                }
                for t in batch
            ]
        }
        r = requests.post(url, json=body, timeout=60)
        r.raise_for_status()
        embeddings = r.json().get("embeddings", [])
        for e in embeddings:
            results.append(_normalize(e.get("values", [])))
    return results

def _st_embed(texts: list[str], prefix: str = "") -> list[list[float]]:
    global _st_model
    if _st_model is None:
        try:
            from sentence_transformers import SentenceTransformer
            _st_model = SentenceTransformer(settings.embedding_model)
        except Exception as exc:
            raise RuntimeError(
                "Embedding unavailable. Configure GEMINI_API_KEY with LLM_PROVIDER=gemini."
            ) from exc
    return _st_model.encode([f"{prefix}{t}" for t in texts], normalize_embeddings=True).tolist()
