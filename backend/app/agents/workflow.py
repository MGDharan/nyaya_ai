from app.agents.multi_agent_pipeline import NyayaMultiAgentPipeline, LegalAgentState, DISCLAIMER

def _fallback(question: str, sources: list[dict], language: str) -> str:
    """Safe fallback routine for offline or degraded states."""
    if not sources:
        return (
            "I could not find a relevant source in the currently ingested legal library. I will not guess the applicable Act or section.\n\n"
            "### 📌 Quick Summary\n"
            "I could not locate an exact matched document in the currently ingested library for this specific issue. "
            "To avoid providing unverified statutory citations, here are the essential next steps.\n\n"
            "### 🗺️ Recommended Action Plan\n"
            "* **Step 1: Note Key Facts** - Identify your State/UT, dates of transaction or incident, and specific names of institutions involved.\n"
            "* **Step 2: Preserve Proof** - Keep bank transaction statements, UPI reference numbers, invoices, or written notices safe.\n"
            "* **Step 3: Consult Official Channels** - Check the official national grievance portal (e.g., National Consumer Helpline at consumerhelpline.gov.in or 1915; Cybercrime portal at cybercrime.gov.in or 1930) or consult an advocate.\n\n"
            f"{DISCLAIMER}"
        )
    lines = [
        "### 📌 Quick Summary",
        "Found potentially relevant legal sources in the indexed library. Review the source passages below.\n",
        "### ⚖️ Retrieved Library Passages"
    ]
    for i, s in enumerate(sources[:4], 1):
        m = s.get("metadata", {})
        lines.append(f"* **{m.get('title','Document')}** ({m.get('status','status unverified')}): {s.get('text','')[:350]}...")
    lines.append("\n### 🗺️ Next Steps")
    lines.append("* Verify the latest Gazette notification, commencement dates, and jurisdiction before relying on these provisions.")
    lines.append(f"\n{DISCLAIMER}")
    return "\n".join(lines)


def run_legal_workflow(question: str, language: str = "English", jurisdiction: str = "India", incident_date: str | None = None, context: str | None = None, query_embedding: list[float] | None = None):
    pipeline = NyayaMultiAgentPipeline()
    state = LegalAgentState(
        question=question,
        language=language,
        jurisdiction=jurisdiction,
        incident_date=incident_date,
        context=context,
        query_embedding=query_embedding
    )
    return pipeline.run(state)
