import hashlib
import json
import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from app.config import settings
from app.services.embeddings import embed_passages, embed_query
from app.services.hybrid_retriever import BM25Retriever, reciprocal_rank_fusion, legal_rerank

# ── SQLite Hybrid Vector Store ────────────────────────────────────────────────

class SQLiteVectorStore:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._bm25 = BM25Retriever()
        self._bm25_initialized = False
        self._init_db()

    def _get_conn(self):
        return sqlite3.connect(str(self.db_path))

    def _init_db(self):
        with self._get_conn() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS chunks (
                    id TEXT PRIMARY KEY,
                    document_id TEXT,
                    chunk_index INTEGER,
                    text TEXT,
                    metadata_json TEXT,
                    embedding_json TEXT
                )
            """)
            conn.commit()

    def count(self) -> int:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM chunks")
            return cur.fetchone()[0]

    def get_all_chunks(self) -> list[dict]:
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT id, text, metadata_json, embedding_json FROM chunks")
            rows = cur.fetchall()

        results = []
        for cid, text, meta_json, emb_json in rows:
            meta = json.loads(meta_json) if meta_json else {}
            emb = json.loads(emb_json) if emb_json else []
            results.append({
                "id": cid,
                "text": text,
                "metadata": meta,
                "embedding": emb
            })
        return results

    def _ensure_bm25(self):
        if not self._bm25_initialized:
            all_docs = self.get_all_chunks()
            self._bm25.fit(all_docs)
            self._bm25_initialized = True

    def upsert(self, ids: list[str], documents: list[str], embeddings: list[list[float]], metadatas: list[dict]):
        with self._get_conn() as conn:
            for chunk_id, doc, emb, meta in zip(ids, documents, embeddings, metadatas):
                conn.execute(
                    """
                    INSERT INTO chunks (id, document_id, chunk_index, text, metadata_json, embedding_json)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(id) DO UPDATE SET
                        text=excluded.text,
                        metadata_json=excluded.metadata_json,
                        embedding_json=excluded.embedding_json
                    """,
                    (
                        chunk_id,
                        meta.get("document_id", ""),
                        meta.get("chunk_index", 0),
                        doc,
                        json.dumps(meta),
                        json.dumps(emb)
                    )
                )
            conn.commit()
        # Invalidate BM25 cache
        self._bm25_initialized = False

    def search_hybrid(self, query: str, query_embedding: list[float], top_k: int = 7, domain: str | None = None) -> list[dict]:
        all_chunks = self.get_all_chunks()
        if not all_chunks:
            return []

        # 1. Vector Search scoring
        vector_scored = []
        for item in all_chunks:
            emb = item["embedding"]
            sim = sum(q * e for q, e in zip(query_embedding, emb)) if emb else 0.0
            dist = max(0.0, 1.0 - sim)
            item_copy = dict(item)
            item_copy["distance"] = float(dist)
            item_copy["similarity"] = float(sim)
            vector_scored.append(item_copy)

        vector_scored.sort(key=lambda x: x["similarity"], reverse=True)
        top_vectors = vector_scored[:top_k * 2]

        # 2. BM25 Search scoring
        self._ensure_bm25()
        bm25_results = self._bm25.search(query, top_k=top_k * 2)

        # 3. Reciprocal Rank Fusion
        fused = reciprocal_rank_fusion(top_vectors, bm25_results, k_rrf=60)

        # 4. Cross-Encoder / Legal Reranking with Domain Filtering
        final_reranked = legal_rerank(query, fused, top_k=top_k, domain=domain)

        # Format output
        rows = []
        for r in final_reranked:
            rows.append({
                "text": r["text"],
                "metadata": r.get("metadata", {}),
                "distance": r.get("distance", 0.5),
                "score": r.get("rerank_score", 0.5)
            })
        return rows


# ── Global Client Resolution ──────────────────────────────────────────────────

_chroma_collection = None
_sqlite_store = None

def _get_store():
    global _chroma_collection, _sqlite_store
    chroma_host = os.environ.get("CHROMA_HOST", "")

    if chroma_host:
        try:
            import chromadb
            client = chromadb.HttpClient(host=chroma_host, port=int(os.environ.get("CHROMA_PORT", "8001")))
            return ("chroma", client.get_or_create_collection("legal_sources", metadata={"hnsw:space": "cosine"}))
        except Exception:
            pass

    try:
        import chromadb
        client = chromadb.PersistentClient(path=settings.chroma_dir)
        return ("chroma", client.get_or_create_collection("legal_sources", metadata={"hnsw:space": "cosine"}))
    except Exception:
        pass

    if _sqlite_store is None:
        db_path = Path(settings.data_dir) / "vectors.db"
        _sqlite_store = SQLiteVectorStore(db_path)
    return ("sqlite", _sqlite_store)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def ingest_chunks(chunks: list[str], metadata: dict, document_id: str) -> int:
    if not chunks:
        return 0
    store_type, store = _get_store()
    ids = [f"{document_id}-{i}" for i in range(len(chunks))]
    base = {k: (v if v is not None else "") for k, v in metadata.items()}
    metadatas = [{**base, "chunk_index": i} for i in range(len(chunks))]
    embeddings = embed_passages(chunks)

    if store_type == "chroma":
        store.upsert(ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadatas)
    else:
        store.upsert(ids=ids, documents=chunks, embeddings=embeddings, metadatas=metadatas)
    return len(chunks)


def search(query: str, top_k: int | None = None, domain: str | None = None) -> list[dict]:
    store_type, store = _get_store()
    k = top_k or settings.top_k

    if store_type == "chroma":
        if store.count() == 0:
            return []
        query_emb = embed_query(query)
        result = store.query(
            query_embeddings=[query_emb],
            n_results=min(k, store.count()),
            include=["documents", "metadatas", "distances"]
        )
        rows = []
        for i, doc in enumerate(result.get("documents", [[]])[0]):
            meta = result.get("metadatas", [[]])[0][i] or {}
            distance = result.get("distances", [[]])[0][i]
            rows.append({"text": doc, "metadata": meta, "distance": float(distance)})
        return rows
    else:
        if store.count() == 0:
            return []
        query_emb = embed_query(query)
        return store.search_hybrid(query, query_emb, top_k=k, domain=domain)
