import argparse, json, uuid
from datetime import datetime, timezone
from pathlib import Path
from app.services.extract import extract_text, chunk_text
from app.services.vector_store import ingest_chunks, sha256_file
from app.config import settings

REGISTRY = Path(settings.data_dir) / "documents.json"

def load_registry():
    if not REGISTRY.exists(): return []
    return json.loads(REGISTRY.read_text(encoding="utf-8"))

def ingest_file(path: Path, title: str | None = None, jurisdiction: str = "India", source_url: str = "", document_type: str = "other", status: str = "unverified"):
    path = path.resolve()
    if not path.exists(): raise FileNotFoundError(path)
    digest = sha256_file(path)
    registry = load_registry()
    existing = next((d for d in registry if d["sha256"] == digest), None)
    if existing: return {"document": existing, "chunks": 0, "duplicate": True}
    text = extract_text(path)
    chunks = chunk_text(text)
    if not chunks: raise ValueError("No text could be extracted")
    doc_id = str(uuid.uuid4())
    metadata = {"document_id": doc_id, "title": title or path.stem, "jurisdiction": jurisdiction,
                "source_url": source_url, "document_type": document_type, "status": status,
                "sha256": digest, "ingested_at": datetime.now(timezone.utc).isoformat()}
    count = ingest_chunks(chunks, metadata, doc_id)
    record = {**metadata, "filename": path.name, "chunks": count}
    registry.append(record)
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")
    return {"document": record, "chunks": count, "duplicate": False}

def main():
    p = argparse.ArgumentParser(description="Ingest a legal source document into NyayaAI RAG")
    p.add_argument("--path", required=True)
    p.add_argument("--title")
    p.add_argument("--jurisdiction", default="India")
    p.add_argument("--source-url", default="")
    p.add_argument("--document-type", default="other")
    p.add_argument("--status", default="unverified")
    a = p.parse_args()
    print(json.dumps(ingest_file(Path(a.path), a.title, a.jurisdiction, a.source_url, a.document_type, a.status), indent=2))

if __name__ == "__main__": main()
