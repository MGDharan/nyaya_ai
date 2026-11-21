# Roadmap to a reliable real-world legal platform

## Stage 1 — MVP (included)
- Upload legal source documents.
- Extract PDF/DOCX/text and chunk them.
- Multilingual semantic retrieval with citations.
- Specialist legal-analysis stages and safe fallback.
- Basic web interface and API.

## Stage 2 — Legal corpus operations
- Build a source catalogue by Central / State / UT jurisdiction and ministry / regulator.
- Add scheduled source discovery for India Code, e-Gazette, Legislative Department, UGC, RBI, SEBI, state gazettes and court websites.
- Fetch candidates into a quarantine queue; never auto-publish a new legal version as active.
- Human reviewer verifies Gazette publication, Act number, section, commencement notification, amendment chain, repeal / savings clauses and effective date.
- Preserve immutable original file, SHA-256, URL, retrieval time, publication date, document version and reviewer.
- Model relationships: `amends`, `repeals`, `substitutes`, `commences`, `made_under`, `interprets`, `overrules`.

## Stage 3 — Structured legal knowledge graph
- PostgreSQL tables: `legal_instrument`, `provision`, `instrument_version`, `gazette_event`, `jurisdiction`, `court_decision`, `citation`, `source_snapshot`, `review_event`.
- Provision-level identifiers and old-to-new mapping (e.g. historical code provisions to successor provisions), reviewed by legal experts.
- Temporal queries: law as on a particular date, not just current text.
- Court precedent retrieval with court, bench, date, case number, holding, treatment and subsequent history.

## Stage 4 — Durable agentic workflow
- Replace sequential orchestrator with LangGraph nodes and persisted checkpoints.
- Add clarification node, conflict-resolution node, source freshness node, lawyer escalation node and human approval gates.
- Separate retrieval from legal interpretation; require source IDs for every legal assertion.
- Add tool permissions. No agent can submit complaints, contact authorities or take legal action without explicit user approval.

## Stage 5 — Model improvement (not blind fine-tuning)
- First create a legally reviewed dataset: question, facts, jurisdiction, date, expected issue, authoritative passages, acceptable answer, forbidden claims, escalation trigger.
- Build retrieval benchmarks: Recall@k, MRR / nDCG, citation precision, citation coverage, temporal correctness and language parity.
- Evaluate base models and multilingual embeddings before fine-tuning.
- Fine-tune a small instruction model with LoRA only on licensed, reviewed examples. Do not train on raw statutes and assume that weights preserve amendment history.
- Keep statutes and judgments in RAG. Model weights are not a reliable update mechanism.
- Run regression tests after every corpus/model update; require lawyer sign-off for high-risk domains.

## Stage 6 — Public deployment
- Threat model, penetration test, privacy impact assessment and DPDP Act compliance review.
- Encrypt user data, isolate case files per account, apply retention/deletion policies, redact logs and provide user export/deletion controls.
- Independent legal review and disclaimer review.
- Monitor stale sources, broken URLs, hallucination rates, harmful advice and answer quality across languages.
