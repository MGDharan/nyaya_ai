# NyayaAI – Legal Document Ingestion & Section-Aware Chunking Pipeline

## 1. Overview & Processing Philosophy

Blind chunking (such as arbitrary 500-token character windows) destroys the hierarchical integrity of Indian legal documents. A section must never be cut in half without preserving its parent Act name, section number, section title, and associated provisos or explanations.

NyayaAI implements a **Section-Aware Hierarchical Statute Chunker** (`app.services.section_chunker`) that parses primary legislation into self-contained statutory units.

---

## 2. Ingestion Stages

```
1. Document Acquisition (PDF, DOCX, TXT, HTML)
   │
   ▼
2. SHA-256 Checksum Calculation & Deduplication
   │
   ▼
3. Text & Layout Extraction (PyMuPDF / docx2txt)
   │
   ▼
4. Language Detection & Normalization
   │
   ▼
5. Section-Aware Hierarchical Parsing
   ├─ Chapter / Part identification
   ├─ Section / Rule / Regulation / Article detection
   ├─ Subsection extraction [(1), (2), (a), (b)]
   ├─ Proviso extraction ["Provided that..."]
   └─ Explanation extraction ["Explanation.- ..."]
   │
   ▼
6. Metadata Enrichment & Official Source Attribution
   ├─ Act title & enactment year
   ├─ Gazette notification reference
   ├─ Commencement date & status (`in_force`)
   └─ Canonical India Code / Court URL
   │
   ▼
7. Dense Vector Embedding Generation (Gemini 768-d)
   │
   ▼
8. Dual Indexing (Okapi BM25 Lexical + Vector Store)
```

---

## 3. Section Chunker Implementation Details

The chunking engine (`backend/app/services/section_chunker.py`) uses regex-based state-machine parsers tuned for Indian legislative drafting standards:

- **Section / Regulation Header Pattern**:
  `r"^(?:Section|Rule|Regulation|Article|Paragraph)?\s*(\d+[A-Za-z]?)\.?\s*[-–—:]?\s*(.+)?$"`
- **Chapter Header Pattern**:
  `r"^(?:CHAPTER|PART)\s+([IVXLCDM\d]+)[\s:.\-]*(.*)?$"`
- **Proviso Extractor**:
  Extracts all conditional clauses beginning with `"Provided that..."` to prevent context detachment.
- **Subsection Extractor**:
  Captures nested clauses `(1)`, `(2)`, `(a)`, `(b)` while retaining their parent section number.

---

## 4. Official Sources Supported

1. **India Code (https://www.indiacode.nic.in)**:
   Canonical digital repository of all Central and State legislation.
2. **e-Gazette of India (https://egazette.gov.in)**:
   Authoritative source for commencement dates, amendments, and notification orders.
3. **University Grants Commission (https://www.ugc.gov.in)**:
   Regulations on student grievances (UGC Regulations 2023), certificate retention notices, and fee refund rules.
4. **Supreme Court of India (https://main.sci.gov.in)**:
   Digital Supreme Court Reports (e-SCR) and landmark judgment digests.
5. **Reserve Bank of India (https://www.rbi.org.in)**:
   Circulars on unauthorized electronic banking transactions and consumer liability.

---

## 5. Ingestion Commands

To ingest a new statute document via CLI:
```bash
python -m app.ingest --path data/sources/consumer_protection_act_2019.pdf \
                     --title "The Consumer Protection Act, 2019" \
                     --jurisdiction "India" \
                     --document-type "statute" \
                     --status "in_force" \
                     --source-url "https://www.indiacode.nic.in/handle/123456789/15256"
```

To re-index all built-in statutory corpora into the local SQLite vector database:
```bash
python scripts/reingest_all.py
```

