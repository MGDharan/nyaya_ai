from pathlib import Path
try:
    import pymupdf as fitz
except ImportError:
    import fitz
from docx import Document

def extract_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        with fitz.open(path) as pdf:
            pages = [p.get_text("text") for p in pdf]
        text = "\n".join(pages)
        if len(text.strip()) < 80:
            raise ValueError("PDF appears scanned or contains too little selectable text. OCR it before ingestion.")
        return text
    if suffix == ".docx":
        doc = Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8", errors="replace")
    raise ValueError("Unsupported file type. Use PDF, DOCX, TXT or MD.")

def chunk_text(text: str, size: int = 1100, overlap: int = 180) -> list[str]:
    text = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    chunks, start = [], 0
    while start < len(text):
        end = min(len(text), start + size)
        if end < len(text):
            boundary = max(text.rfind("\n", start, end), text.rfind(". ", start, end))
            if boundary > start + size // 2:
                end = boundary + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        start = max(start + 1, end - overlap)
    return chunks
