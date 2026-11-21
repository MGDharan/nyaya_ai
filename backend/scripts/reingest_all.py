import sys
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

import uuid
from app.services.statute_corpus import STATUTE_DOCUMENTS
from app.services.section_chunker import chunk_legal_statute_section_aware
from app.services.vector_store import SQLiteVectorStore
from app.config import settings

def reingest():
    db_path = Path(settings.data_dir) / "vectors.db"
    store = SQLiteVectorStore(db_path)
    
    # Clear existing chunks for clean reindex
    with store._get_conn() as conn:
        conn.execute("DELETE FROM chunks")
        conn.commit()

    total_chunks = 0
    for doc in STATUTE_DOCUMENTS:
        chunks = chunk_legal_statute_section_aware(doc["text"], default_act_title=doc["title"])
        doc_id = str(uuid.uuid4())
        ids = [f"{doc_id}-{i}" for i in range(len(chunks))]
        texts = [c["text"] for c in chunks]
        metadatas = [
            {
                "title": doc["title"],
                "section_number": c.get("section_number", ""),
                "jurisdiction": doc.get("jurisdiction", "India"),
                "document_type": doc.get("document_type", "statute"),
                "status": doc.get("status", "in_force"),
                "source_url": doc.get("source_url", ""),
                "act_number": doc.get("act_number", "")
            }
            for c in chunks
        ]
        # Store with zero vector fallback for offline embeddings
        embeddings = [[0.0] * 768 for _ in chunks]
        store.upsert(ids=ids, documents=texts, embeddings=embeddings, metadatas=metadatas)
        total_chunks += len(chunks)
        print(f"Ingested '{doc['title']}': {len(chunks)} chunks.")

    print(f"\nSuccessfully indexed {total_chunks} legal section chunks in SQLiteVectorStore.")

if __name__ == "__main__":
    reingest()

