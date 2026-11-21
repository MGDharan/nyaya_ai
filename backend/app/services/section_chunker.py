"""
Section-Aware Hierarchical Chunking & Ingestion for Indian Statutes.
Preserves Act, Chapter, Section, Subsection, Proviso, and Explanations.
"""

import re
from typing import List, Dict, Any, Optional
from pathlib import Path


class LegalSectionChunk:
    def __init__(
        self,
        act_name: str,
        section_number: str,
        section_title: str,
        text: str,
        chapter: Optional[str] = None,
        subsections: Optional[List[str]] = None,
        provisos: Optional[List[str]] = None,
        explanations: Optional[List[str]] = None
    ):
        self.act_name = act_name
        self.section_number = section_number
        self.section_title = section_title
        self.text = text
        self.chapter = chapter or ""
        self.subsections = subsections or []
        self.provisos = provisos or []
        self.explanations = explanations or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "act_name": self.act_name,
            "section_number": self.section_number,
            "section_title": self.section_title,
            "text": self.text,
            "chapter": self.chapter,
            "subsections": self.subsections,
            "provisos": self.provisos,
            "explanations": self.explanations
        }


def chunk_legal_statute_section_aware(raw_text: str, default_act_title: str = "Indian Statute") -> List[Dict[str, Any]]:
    """
    Parses full legislative text into discrete section-level structured chunks.
    Detects:
    - Chapter X / Part Y
    - Section [0-9A-Z]+. Title
    - Subsections (1), (2), (a), (b)
    - Provided that... (Provisos)
    - Explanation.- ...
    """
    lines = raw_text.splitlines()
    chunks: List[Dict[str, Any]] = []

    current_chapter = ""
    current_sec_num = ""
    current_sec_title = ""
    current_sec_lines = []

    # Section / Rule / Regulation / Article regex
    sec_pattern = re.compile(r"^(?:Section|Rule|Regulation|Article|Paragraph)?\s*(\d+[A-Za-z]?)\.?\s*[-–—:]?\s*(.+)?$", re.IGNORECASE)
    chapter_pattern = re.compile(r"^(?:CHAPTER|PART)\s+([IVXLCDM\d]+)[\s:.\-]*(.*)?$", re.IGNORECASE)

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        # Check Chapter header
        chap_match = chapter_pattern.match(stripped)
        if chap_match:
            current_chapter = f"Chapter {chap_match.group(1)}: {chap_match.group(2) or ''}".strip()
            continue

        # Check Section header
        sec_match = sec_pattern.match(stripped)
        # Verify it looks like a genuine section title (not an inline numbered list)
        is_candidate_sec = bool(sec_match) and len(stripped) < 180 and not stripped.endswith(",") and not stripped.endswith(";")

        if is_candidate_sec and sec_match:
            # Land prior section if accumulated
            if current_sec_num and current_sec_lines:
                sec_text = "\n".join(current_sec_lines).strip()
                if len(sec_text) > 30:
                    chunks.append({
                        "act_name": default_act_title,
                        "chapter": current_chapter,
                        "section_number": current_sec_num,
                        "section_title": current_sec_title,
                        "text": f"{default_act_title} - Section {current_sec_num}: {current_sec_title}\n{sec_text}",
                        "subsections": _extract_subsections(sec_text),
                        "provisos": _extract_provisos(sec_text)
                    })

            current_sec_num = sec_match.group(1)
            current_sec_title = (sec_match.group(2) or "").strip()
            current_sec_lines = []
            continue

        if current_sec_num:
            current_sec_lines.append(stripped)
        else:
            # Preamble / preliminary definitions before Section 1
            current_sec_lines.append(stripped)

    # Flush final accumulated section
    if current_sec_num and current_sec_lines:
        sec_text = "\n".join(current_sec_lines).strip()
        if len(sec_text) > 30:
            chunks.append({
                "act_name": default_act_title,
                "chapter": current_chapter,
                "section_number": current_sec_num,
                "section_title": current_sec_title,
                "text": f"{default_act_title} - Section {current_sec_num}: {current_sec_title}\n{sec_text}",
                "subsections": _extract_subsections(sec_text),
                "provisos": _extract_provisos(sec_text)
            })
    elif current_sec_lines and not chunks:
        # Fallback to standard sliding window chunker if statutory pattern not detected
        full_text = "\n".join(current_sec_lines)
        from app.services.extract import chunk_text
        raw_chunks = chunk_text(full_text)
        for idx, rc in enumerate(raw_chunks):
            chunks.append({
                "act_name": default_act_title,
                "chapter": "",
                "section_number": f"Part-{idx+1}",
                "section_title": "General Provision",
                "text": rc,
                "subsections": [],
                "provisos": []
            })

    return chunks


def _extract_subsections(text: str) -> List[str]:
    return re.findall(r"\(\d+\)\s+[^\(\)]+", text)


def _extract_provisos(text: str) -> List[str]:
    return re.findall(r"Provided that[^\.]+\.", text, re.IGNORECASE)
