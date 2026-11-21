from app.services.extract import chunk_text
from app.agents.workflow import _fallback, DISCLAIMER

def test_chunk_text_returns_content():
    chunks = chunk_text("Section 1. This is a legal provision.\n" * 100, size=180, overlap=30)
    assert chunks and all(c.strip() for c in chunks)

def test_no_source_fallback_does_not_invent_law():
    answer = _fallback("My issue", [], "English")
    assert "could not find a relevant source" in answer
    assert "will not guess" in answer
    assert DISCLAIMER in answer
