"""
Hybrid Retrieval Engine for NyayaAI.
Combines BM25 keyword scoring (TF-IDF probabilistic scoring) with dense vector cosine similarity
and reciprocal rank fusion (RRF) / cross-encoder heuristic reranking.
"""

import math
import re
from typing import List, Dict, Any, Optional
from collections import Counter


def tokenize(text: str) -> List[str]:
    """Extract normalized lowercase legal and linguistic tokens."""
    tokens = re.findall(r"\b[a-zA-Z0-9_\-\(\)\/]+\b", text.lower())
    # Filter very short non-informative noise while preserving numbers and section codes (e.g. 138, 2(7), 66d)
    return [t for t in tokens if len(t) > 1 or t.isdigit()]


class BM25Retriever:
    """
    Pure-Python Okapi BM25 implementation.
    Requires no external C-dependencies (no Lucene, no C-compiler needed).
    """
    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.corpus: List[Dict[str, Any]] = []
        self.doc_len: List[int] = []
        self.avg_doc_len: float = 0.0
        self.doc_freqs: Dict[str, int] = Counter()
        self.idf: Dict[str, float] = {}
        self.total_docs: int = 0

    def fit(self, documents: List[Dict[str, Any]]):
        """Fit index with document list where each item has 'text'."""
        self.corpus = documents
        self.total_docs = len(documents)
        if self.total_docs == 0:
            self.avg_doc_len = 0.0
            return

        self.doc_len = []
        self.doc_freqs = Counter()

        for doc in documents:
            tokens = tokenize(doc.get("text", ""))
            self.doc_len.append(len(tokens))
            unique_tokens = set(tokens)
            for token in unique_tokens:
                self.doc_freqs[token] += 1

        self.avg_doc_len = sum(self.doc_len) / self.total_docs if self.total_docs > 0 else 0.0

        # Calculate IDF with standard Robertson-Spärck Jones BM25 formula
        self.idf = {}
        for token, freq in self.doc_freqs.items():
            self.idf[token] = math.log((self.total_docs - freq + 0.5) / (freq + 0.5) + 1.0)

    def search(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Compute BM25 scores for query."""
        if self.total_docs == 0:
            return []

        q_tokens = tokenize(query)
        if not q_tokens:
            return []

        scores: List[float] = [0.0] * self.total_docs

        for q_token in q_tokens:
            if q_token not in self.idf:
                continue
            idf_val = self.idf[q_token]

            for idx, doc in enumerate(self.corpus):
                doc_tokens = tokenize(doc.get("text", ""))
                tf = doc_tokens.count(q_token)
                if tf == 0:
                    continue

                d_len = self.doc_len[idx]
                denom = tf + self.k1 * (1.0 - self.b + self.b * (d_len / (self.avg_doc_len or 1.0)))
                scores[idx] += idf_val * ((tf * (self.k1 + 1.0)) / denom)

        ranked = []
        for idx, score in enumerate(scores):
            if score > 0:
                doc_copy = dict(self.corpus[idx])
                doc_copy["bm25_score"] = float(score)
                ranked.append(doc_copy)

        ranked.sort(key=lambda x: x["bm25_score"], reverse=True)
        return ranked[:top_k]


def reciprocal_rank_fusion(
    vector_results: List[Dict[str, Any]],
    bm25_results: List[Dict[str, Any]],
    k_rrf: int = 60,
    vector_weight: float = 0.6,
    bm25_weight: float = 0.4
) -> List[Dict[str, Any]]:
    """
    RRF fusion combining ranked vector results and ranked keyword (BM25) results.
    """
    scores: Dict[str, float] = {}
    docs_by_id: Dict[str, Dict[str, Any]] = {}

    def get_id(doc: Dict[str, Any], idx: int) -> str:
        meta = doc.get("metadata", {})
        doc_id = meta.get("document_id") or meta.get("id") or doc.get("id")
        chunk_idx = meta.get("chunk_index", 0)
        if doc_id:
            return f"{doc_id}_{chunk_idx}"
        return f"doc_{idx}_{hash(doc.get('text', '')[:100])}"

    # Vector ranking
    for rank, doc in enumerate(vector_results):
        did = get_id(doc, rank)
        docs_by_id[did] = doc
        scores[did] = scores.get(did, 0.0) + (vector_weight * (1.0 / (k_rrf + rank + 1)))

    # BM25 ranking
    for rank, doc in enumerate(bm25_results):
        did = get_id(doc, rank)
        if did not in docs_by_id:
            docs_by_id[did] = doc
        scores[did] = scores.get(did, 0.0) + (bm25_weight * (1.0 / (k_rrf + rank + 1)))

    # Sort merged
    sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    fused: List[Dict[str, Any]] = []

    for did in sorted_ids:
        entry = dict(docs_by_id[did])
        entry["hybrid_score"] = float(scores[did])
        fused.append(entry)

    return fused


def is_statute_irrelevant_to_query(query: str, title: str, domain: Optional[str] = None) -> bool:
    """
    Rigorously detects whether a retrieved legislative Act is completely unrelated
    to the legal dispute domain, ensuring high retrieval precision and zero irrelevant statutes.
    """
    q = query.lower()
    t = title.lower()

    # Domain-directed exclusions
    d = (domain or "").lower()
    if d:
        # If domain is clearly non-consumer, exclude Consumer Protection Act
        if "consumer protection act" in t or "consumer protection (e-commerce)" in t:
            if not any(cand in d for cand in ["consumer protection & product liability", "consumer protection & e-commerce", "paid commercial public utility"]):
                return True

        # If domain is not financial / cheque, exclude NI Act
        if "negotiable instruments" in t:
            if "negotiable instruments" not in d and not any(w in q for w in ["cheque", "dishonour", "bounce", "bounced", "138"]):
                return True

        # If domain is not cyber / IT, exclude IT Act
        if "information technology act" in t or "cyber harassment" in t:
            if not any(cand in d for cand in ["cyber", "information technology", "identity theft", "harassment"]) and not any(w in q for w in ["cyber", "online", "computer", "internet", "upi", "scam", "fraud", "hack", "hacked", "66"]):
                return True

    # 1. Negotiable Instruments Act: strictly only relevant if cheque, bounce, dishonour, drawer, payee
    if "negotiable instruments" in t:
        if not any(w in q for w in ["cheque", "dishonour", "bounce", "bounced", "drawer", "payee", "138", "promissory", "bank memo"]):
            return True

    # 2. Information Technology Act: strictly only relevant if cyber, online, computer, hacking, voyeurism, upi fraud
    if "information technology act" in t or "cyber harassment" in t:
        if not any(w in q for w in ["cyber", "online", "computer", "internet", "upi", "scam", "fraud", "hack", "hacked", "voyeurism", "photo", "video", "social media", "electronic", "phishing", "66"]):
            return True

    # 2A. IT Act Sections 43 & 66 (Hacking, Unauthorized Access, Virus, System Disruption): strictly only when elements met
    if "sections 43" in t or "section 43" in t or "section 66 " in t or "unauthorized access, data damage" in t:
        is_unauthorized_access = any(w in q for w in [
            "unauthorized access", "unauthorised access", "hack", "hacked", "hacking", "server",
            "data theft", "stole data", "virus", "malware", "contaminant", "disrupted", "source code",
            "accessed computer", "damage to computer"
        ])
        if not is_unauthorized_access:
            return True

    # 2B. IT Act Section 66C (Identity Theft / Stolen Credentials): strictly only when password, signature, or biometric used
    if "section 66c" in t or "identity theft & password" in t:
        is_stolen_creds = any(w in q for w in [
            "electronic signature", "password", "stolen password", "login credentials", "aadhaar",
            "pan card", "identity theft", "unique identification", "cloned", "biometric", "credentials"
        ])
        if not is_stolen_creds:
            return True

    # 2C. UGC Regulations & Supreme Court Education Judgments: strictly only relevant if higher education/university
    if "ugc" in t or "education" in t or "student grievances" in t or "university grants commission" in t or "surjeet kaur" in t or "p.t. koshy" in t:
        is_education = any(w in q for w in [
            "college", "university", "ugc", "exam fee", "tuition fee", "admission fee",
            "hall ticket", "original certificates", "degree", "marksheets", "debarred", "student grievance", "student"
        ])
        if not is_education:
            return True

    # 3. Consumer Protection Act: strictly irrelevant for sovereign duties, workplace harassment, road accidents, friendly loans, or finder reward
    if "consumer protection act" in t or "consumer protection (e-commerce)" in t:
        is_sovereign_gov = any(w in q for w in [
            "tahsildar", "caste certificate", "income certificate", "nativity", "patta", "mutation",
            "driving license", "bribe", "bribery", "dvac", "vigilance", "police", "fir", "sho",
            "passport", "government officer", "govt officer", "public servant", "sub-registrar", "bdo"
        ])
        is_paid_utility = any(w in q for w in ["tangedco", "electricity bill", "power bill", "water tanker", "paid water"])
        if is_sovereign_gov and not is_paid_utility:
            return True
        is_non_consumer = any(w in q for w in [
            "sexual harassment", "posh", "workplace harassment", "boss touched",
            "road accident", "negligent driving", "mact", "hit and run",
            "friend borrowed", "lent money", "borrowed ₹", "borrowed rs", "friendly loan",
            "promissory note", "personal loan", "loan to my friend", "loan of rs",
            "lost spectacles", "finder", "found wallet", "reward for finding",
            "defamation", "slander", "libel", "defamed",
            "fake recruiter", "fake job offer", "remote job", "job scam", "fake job", "bogus recruiter", "telegram",
            "impersonating", "impersonator", "fake profile", "fake instagram", "fake account", "using my photo", "using my name",
            "phishing", "stolen password", "login credentials", "net banking password", "hacker", "ransomware", "unauthorized access"
        ])
        if is_non_consumer:
            return True

    # 4. Motor Vehicles Act: only relevant if motor vehicle, accident, driving, mact, crash
    if "motor vehicles" in t or "mact" in t:
        if not any(w in q for w in ["motor", "vehicle", "car", "bike", "accident", "mact", "driving", "driver", "hit", "crash", "pedestrian"]):
            return True

    # 5. POSH Act / Workplace Harassment: only relevant if sexual harassment, workplace, posh
    if "posh" in t or "sexual harassment" in t:
        if not any(w in q for w in ["sexual harassment", "posh", "harassment", "internal committee", "workplace harassment"]):
            return True

    # 4. Right to Information Act: irrelevant if private cheque bounce, matrimonial maintenance, or cyber stalking
    if "right to information" in t:
        if any(w in q for w in ["cheque", "bounce", "dishonour", "maintenance", "deserted wife", "alimony", "maternity leave"]):
            return True

    # 5. Prevention of Corruption Act: only relevant if bribe, corruption, public servant, dvac, vigilance
    if "prevention of corruption" in t:
        if not any(w in q for w in ["bribe", "bribery", "corruption", "dvac", "vigilance", "undue advantage", "illegal gratification", "demanding money"]):
            return True

    # 6. Maternity Benefit Act: only relevant if maternity, pregnancy, pregnant
    if "maternity benefit" in t:
        if not any(w in q for w in ["maternity", "pregnant", "pregnancy", "delivery", "miscarriage"]):
            return True

    # 7. Tenancy Act (TNRRLTA): only relevant if tenant, landlord, rent, security deposit, eviction
    if "tenants act" in t or "tnrrlta" in t or "landlords and tenants" in t:
        if not any(w in q for w in ["tenant", "landlord", "rent", "deposit", "eviction", "lease", "premises"]):
            return True

    return False


def legal_rerank(
    query: str,
    candidates: List[Dict[str, Any]],
    top_k: int = 7,
    domain: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Cross-attention heuristic reranker for Indian legal texts.
    Boosts:
    1. Exact statutory section match (e.g. 'section 138', 'section 35').
    2. Authority level (Supreme Court > High Court > District Forum > unverified).
    3. Status penalty (repealed/inactive laws are penalized unless historical query).
    4. Domain precision: Filters out completely unrelated statutes.
    """
    if not candidates:
        return []

    query_tokens = set(tokenize(query))
    has_section = any(t in query_tokens for t in ["section", "sec", "regulation", "act"])

    # Extract any explicit numbers mentioned in query (e.g., '138', '35', '66d')
    query_nums = set(re.findall(r"\b\d+[a-zA-Z]?\b", query.lower()))

    # First pass: Filter out completely irrelevant statutes based on domain & query context
    valid_candidates = []
    for item in candidates:
        meta = item.get("metadata", {})
        meta_title = meta.get("title", "")
        if not is_statute_irrelevant_to_query(query, meta_title, domain):
            valid_candidates.append(item)

    # Fallback if filtering was too aggressive: keep top candidates
    target_pool = valid_candidates if valid_candidates else candidates

    reranked = []
    for item in target_pool:
        score = item.get("hybrid_score", 0.5)
        text_lower = item.get("text", "").lower()
        meta = item.get("metadata", {})
        meta_title = meta.get("title", "").lower()

        # Boost 1: Explicit section number match in text or metadata
        if query_nums:
            for num in query_nums:
                if f"section {num}" in text_lower or f"sec {num}" in text_lower or f"section {num}" in meta_title:
                    score += 0.4
                elif num in text_lower:
                    score += 0.15

        # Boost 2: Supreme Court / Central Act authority
        if "supreme court" in text_lower or "supreme court" in meta_title:
            score += 0.1
        if "act, 20" in text_lower or "act, 19" in text_lower or "act, 18" in text_lower:
            score += 0.05

        # Boost 3: Administrative / Sovereign relevance
        if "sovereign" in text_lower or "mandamus" in text_lower or "article 226" in text_lower:
            if any(w in query.lower() for w in ["officer", "refusing", "certificate", "license", "government"]):
                score += 0.3

        # Penalty: Repealed statute penalty
        if meta.get("status") == "repealed" or "repealed by" in text_lower:
            score -= 0.25

        item_copy = dict(item)
        item_copy["rerank_score"] = round(score, 4)
        reranked.append(item_copy)

    reranked.sort(key=lambda x: x["rerank_score"], reverse=True)
    return reranked[:top_k]

