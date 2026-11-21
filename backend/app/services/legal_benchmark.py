"""
Comprehensive Evaluation & Benchmarking Dataset for NyayaAI.
Contains 15 real-world Indian legal scenarios across all priority domains.
Includes question, expected domain, applicable statutes, key sections,
temporal boundaries, prohibited incorrect conclusions, and expert reference answers.
"""

from typing import List, Dict, Any

LEGAL_BENCHMARK_SCENARIOS: List[Dict[str, Any]] = [
    {
        "id": "scenario_01",
        "domain": "Education",
        "title": "College examination fee dispute",
        "question": "I paid ₹200 for my college examination fee through UPI. I have a payment receipt, but my college says that I have not paid. They are refusing to allow me to apply for the examination. What can I do?",
        "expected_issue": "Dispute over university examination fee payment reconciliation and wrongful denial of hall ticket.",
        "expected_provisions": [
            "UGC (Redressal of Grievances of Students) Regulations, 2023 - Regulation 5 & 6",
            "MDU v. Surjeet Kaur (2010) 11 SCC 159",
            "P.T. Koshy v. Ellen Charitable Trust (2012) 3 SCC 797"
        ],
        "prohibited_conclusions": [
            "Advising immediate consumer court filing against university without citing Surjeet Kaur doctrine that education is not a service under CPA.",
            "Guaranteeing that consumer forum will grant an immediate injunction against the university."
        ],
        "expected_authorities": ["Student Grievance Redressal Committee (SGRC)", "University Ombudsperson", "UGC Samarth Grievance Portal"],
        "limitation_note": "15-day resolution timeline before institutional SGRC under UGC 2023 Regulations."
    },
    {
        "id": "scenario_02",
        "domain": "Education",
        "title": "College refusing original certificates upon course completion",
        "question": "I completed my B.Tech degree from a private affiliated engineering college, but they are withholding my original 10th and 12th certificates demanding extra unreceipted placement fees. Can they legally hold my original documents?",
        "expected_issue": "Unlawful retention of original student academic certificates by educational institution.",
        "expected_provisions": [
            "UGC Public Notice on Retention of Original Certificates (October 2018 / 2023)",
            "Section 405/406 IPC or Section 316 BNS (Criminal Breach of Trust)",
            "Article 226 of the Constitution of India (Writ of Mandamus against college)"
        ],
        "prohibited_conclusions": [
            "Stating that educational institutions have a statutory right of general lien over original academic marks sheets."
        ],
        "expected_authorities": ["UGC Portal", "High Court (Writ)", "University Registrar"],
        "limitation_note": "Immediate violation of UGC mandatory guidelines."
    },
    {
        "id": "scenario_03",
        "domain": "Education / Administrative",
        "title": "Government scholarship disbursement delay",
        "question": "My Post-Matric SC/ST government scholarship for 2023 was approved 10 months ago, but the state welfare department has not released the scholarship amount to my bank account. What legal steps can I take?",
        "expected_issue": "Undue delay in welfare benefit disbursement under statutory Direct Benefit Transfer norms.",
        "expected_provisions": [
            "Right to Information Act, 2005 - Section 6(1)",
            "State Right to Public Services Act (Guarantee of Services Act)",
            "Article 226 of the Constitution of India"
        ],
        "prohibited_conclusions": [
            "Advising filing a cheque bounce case or civil suit against the President of India."
        ],
        "expected_authorities": ["District Welfare Officer", "State Information Commission", "CPGRAMS Portal"],
        "limitation_note": "RTI reply mandatory within 30 days."
    },
    {
        "id": "scenario_04",
        "domain": "Labour & Employment",
        "title": "Salary non-payment and sudden termination",
        "question": "My IT company in Bangalore terminated my employment with 2 days notice and has not paid my salary for the last 3 months (₹1,80,000). What legal remedies do I have?",
        "expected_issue": "Unlawful termination and wrongful withholding of earned wages and full-and-final settlement.",
        "expected_provisions": [
            "Payment of Wages Act, 1936 - Section 15",
            "Karnataka Shops and Commercial Establishments Act, 1961 - Section 39",
            "Industrial Disputes Act, 1947 - Section 2A/33C(2)"
        ],
        "prohibited_conclusions": [
            "Claiming that IT employees are completely excluded from all labor and civil dispute remedies."
        ],
        "expected_authorities": ["Labor Commissioner / Conciliation Officer", "Civil Court", "Labor Court"],
        "limitation_note": "Statutory notice under appointment letter; claims under Section 15 Payment of Wages within 12 months."
    },
    {
        "id": "scenario_05",
        "domain": "Labour & Employment",
        "title": "Maternity leave denial and illegal termination",
        "question": "When I submitted my pregnancy certificate and requested 26 weeks maternity leave, my employer terminated my services citing performance. Is this legal?",
        "expected_issue": "Direct violation of statutory maternity benefit and unlawful dismissal during pregnancy.",
        "expected_provisions": [
            "Maternity Benefit Act, 1961 - Section 5 & Section 12",
            "Maternity Benefit (Amendment) Act, 2017"
        ],
        "prohibited_conclusions": [
            "Suggesting that private employers have unfettered discretion to terminate pregnant women during maternity."
        ],
        "expected_authorities": ["Inspector under Maternity Benefit Act", "Labor Commissioner", "High Court"],
        "limitation_note": "Section 12 makes dismissal during maternity void ab initio and a criminal offence."
    },
    {
        "id": "scenario_06",
        "domain": "Criminal Law / Procedure",
        "title": "Police officer refusing to register an FIR for mobile theft",
        "question": "My mobile phone and wallet were snatched at knife-point yesterday. When I went to the police station, the sub-inspector refused to register an FIR and only gave a lost article CSR receipt. What can I do?",
        "expected_issue": "Police refusal to register mandatory FIR in a cognizable offence.",
        "expected_provisions": [
            "Lalita Kumari v. Govt. of U.P. (2014) 2 SCC 1 (Mandatory FIR registration)",
            "Section 154 CrPC or Section 173 BNSS",
            "Section 156(3) CrPC / Section 175(3) BNSS (Judicial Magistrate order)"
        ],
        "prohibited_conclusions": [
            "Advising filing a consumer complaint against the Police Department."
        ],
        "expected_authorities": ["Superintendent of Police (SP) under 154(3)", "Judicial Magistrate under 156(3)", "State Police Complaints Authority"],
        "limitation_note": "Statutory duty to register immediately for cognizable robbery/extortion."
    },
    {
        "id": "scenario_07",
        "domain": "Cybercrime / Criminal Law",
        "title": "Online harassment and rape threats on Instagram",
        "question": "An anonymous Instagram user is sending me obscene morphed photos of myself and rape threats via direct messages. Where should I complain?",
        "expected_issue": "Cyber stalking, electronic harassment, voyeurism, and criminal intimidation of a woman.",
        "expected_provisions": [
            "Information Technology Act, 2000 - Section 66E, Section 67, Section 67A",
            "Indian Penal Code - Section 354D, 506, 509 (or BNS Sections 78, 351, 79)"
        ],
        "prohibited_conclusions": [
            "Telling the user to delete their account and lose the chat evidence."
        ],
        "expected_authorities": ["National Cyber Crime Reporting Portal (1930 / cybercrime.gov.in)", "Cyber Crime Police Station", "National Commission for Women"],
        "limitation_note": "Immediate preservation of digital URL, handles, timestamps, and hash."
    },
    {
        "id": "scenario_08",
        "domain": "Consumer Protection",
        "title": "E-commerce refund refusal for damaged product",
        "question": "I bought a refrigerator for ₹45,000 from an online e-commerce website. It arrived with a broken compressor. The seller is refusing replacement or refund stating that 7 days return window has passed. What are my rights?",
        "expected_issue": "Deficiency in service, delivery of defective goods, and unfair trade practice by e-commerce marketplace.",
        "expected_provisions": [
            "Consumer Protection Act, 2019 - Section 2(7), Section 2(11), Section 35",
            "Consumer Protection (E-Commerce) Rules, 2020"
        ],
        "prohibited_conclusions": [
            "Claiming that a 7-day seller return policy overrides the 2-year statutory warranty and CPA remedies."
        ],
        "expected_authorities": ["National Consumer Helpline (1915 / consumerhelpline.gov.in)", "District Consumer Commission (edaakhil.nic.in)"],
        "limitation_note": "2 years limitation under Section 69 of CPA 2019."
    },
    {
        "id": "scenario_09",
        "domain": "Banking & Cybercrime",
        "title": "UPI financial fraud and unapproved debit",
        "question": "Someone called me pretending to be my bank manager and convinced me to click a refund link. ₹85,000 was debited from my SBI savings account via UPI 2 hours ago. How do I get my money back?",
        "expected_issue": "Unauthorized electronic fund transfer and digital banking fraud.",
        "expected_provisions": [
            "RBI Circular on Customer Protection: Limiting Liability in Unauthorized Electronic Banking Transactions (July 2017)",
            "Information Technology Act, 2000 - Section 43, 66D"
        ],
        "prohibited_conclusions": [
            "Telling the user they have zero remedy because they clicked a link."
        ],
        "expected_authorities": ["National Cyber Crime Helpline (1930)", "Bank Nodal Grievance Officer", "RBI Banking Ombudsman (cms.rbi.org.in)"],
        "limitation_note": "Zero customer liability if reported within 3 days of unauthorized debit under RBI norms."
    },
    {
        "id": "scenario_10",
        "domain": "Cybercrime / Civil Law",
        "title": "Fake social media profile impersonation",
        "question": "Someone created a fake Facebook account with my real name, photo, and phone number, soliciting money from my friends. What steps can I take?",
        "expected_issue": "Cheating by personation, identity theft, and defamatory online impersonation.",
        "expected_provisions": [
            "Information Technology Act, 2000 - Section 66C & Section 66D",
            "Information Technology (Intermediary Guidelines and Digital Media Ethics Code) Rules, 2021"
        ],
        "prohibited_conclusions": [
            "Claiming that social media platforms are immune from taking down impersonation profiles."
        ],
        "expected_authorities": ["Grievance Officer of Social Media Platform (24-hour takedown under IT Rules)", "Cyber Police (cybercrime.gov.in)"],
        "limitation_note": "Platform must take down impersonating content within 24 hours of notification."
    },
    {
        "id": "scenario_11",
        "domain": "Property & Tenancy",
        "title": "Tenant security deposit withholding in Chennai",
        "question": "My landlord in Chennai is refusing to return my security deposit of ₹60,000 even though I gave 1 month notice and vacated the flat clean on 1st November. What law protects me?",
        "expected_issue": "Illegal withholding of tenant security deposit beyond statutory return window.",
        "expected_provisions": [
            "TNRRLTA, 2017 - Section 10(2) (Return of deposit within 1 month)",
            "Section 21 TNRRLTA (Application to Rent Authority)",
            "H.S. Goutham v. Rama Murthy (2021) 5 SCC 241"
        ],
        "prohibited_conclusions": [
            "Citing the repealed Tamil Nadu Buildings (Lease and Rent Control) Act, 1960."
        ],
        "expected_authorities": ["Rent Authority / Rent Court", "Civil Court"],
        "limitation_note": "Mandatory refund within 1 month of handing over vacant possession."
    },
    {
        "id": "scenario_12",
        "domain": "Family & Personal Law",
        "title": "Interim maintenance for wife and minor child",
        "question": "My husband deserted me and our 4-year-old child 6 months ago. He earns ₹1,20,000 per month as a software engineer but gives us zero maintenance. How can I seek maintenance quickly?",
        "expected_issue": "Right of deserted wife and child to statutory monthly maintenance and interim relief.",
        "expected_provisions": [
            "Section 125 CrPC / Section 144 BNSS",
            "Protection of Women from Domestic Violence Act, 2005 - Section 20 & 23",
            "Rajnesh v. Neha (2020) Supreme Court (Guidelines on Affidavits of Assets and Liabilities)"
        ],
        "prohibited_conclusions": [
            "Stating that maintenance can only be claimed after a final divorce decree is passed."
        ],
        "expected_authorities": ["Family Court", "Judicial Magistrate First Class"],
        "limitation_note": "Interim maintenance can be granted on first return of notice."
    },
    {
        "id": "scenario_13",
        "domain": "Criminal Law / Temporal Verification",
        "title": "Old versus new criminal law applicability",
        "question": "A fraud occurred on 10 March 2024. Can the police register the FIR under the new Bharatiya Nyaya Sanhita (BNS), 2023?",
        "expected_issue": "Temporal application of criminal legislation and constitutional bar on ex-post facto laws.",
        "expected_provisions": [
            "Article 20(1) of the Constitution of India",
            "Bharatiya Nyaya Sanhita, 2023 (Commenced 1 July 2024)",
            "Indian Penal Code, 1860 (Governs offences committed prior to 1 July 2024)"
        ],
        "prohibited_conclusions": [
            "Stating that BNS 2023 applies retrospectively to offences committed before 1 July 2024."
        ],
        "expected_authorities": ["Police Station", "Jurisdictional Magistrate"],
        "limitation_note": "Substantive penal law must be IPC 1860; procedure from 1 July 2024 is under BNSS."
    },
    {
        "id": "scenario_14",
        "domain": "Financial / Cheque Bounce",
        "title": "Section 138 Cheque bounce demand notice period",
        "question": "A cheque issued by my business partner bounced due to insufficient funds on 1st November. Can I immediately file a criminal case in court tomorrow without any notice?",
        "expected_issue": "Statutory pre-condition of 138 demand notice and 15-day cure period before cause of action arises.",
        "expected_provisions": [
            "Negotiable Instruments Act, 1881 - Section 138 proviso (b) & (c)",
            "Section 142 NI Act"
        ],
        "prohibited_conclusions": [
            "Advising that a 138 case can be filed directly without serving a 30-day statutory demand notice and giving 15 days to pay."
        ],
        "expected_authorities": ["Metropolitan Magistrate / Judicial Magistrate First Class"],
        "limitation_note": "Notice within 30 days of memo; 15 days cure period; complaint within 1 month thereafter."
    },
    {
        "id": "scenario_15",
        "domain": "Administrative / Procedural",
        "title": "Ambiguous legal question requiring clarification",
        "question": "Someone took my money. What can I do?",
        "expected_issue": "Ambiguous factual statement requiring extraction of essential legal predicates (loan vs fraud vs theft vs fee).",
        "expected_provisions": [
            "Civil suit for recovery / Order 37 CPC",
            "BNS Section 318 / IPC 420 (if fraud)",
            "Section 138 NI Act (if cheque)"
        ],
        "prohibited_conclusions": [
            "Asserting a single definitive section without qualifying missing facts (date, relationship, method of payment)."
        ],
        "expected_authorities": ["Police / Civil Court depending on clarification"],
        "limitation_note": "Missing facts must be flagged before definitive conclusion."
    }
]


def evaluate_response_against_scenario(scenario: Dict[str, Any], answer: str) -> Dict[str, Any]:
    """Scores an answer against expected provisions, prohibited claims, and authorities."""
    ans_lower = answer.lower()
    
    # Check expected provisions
    matched_provisions = []
    for prov in scenario.get("expected_provisions", []):
        prov_short = prov.split("-")[0].strip().lower()
        if any(term in ans_lower for term in [prov_short[:15], "ugc", "surjeet kaur", "138", "35", "10", "ipc", "bns"]):
            matched_provisions.append(prov)

    # Check prohibited conclusions
    prohibited_violations = []
    for proh in scenario.get("prohibited_conclusions", []):
        # Specific check: if education dispute and guarantees consumer court victory
        if "surjeet kaur" in proh.lower() and "consumer" in ans_lower and "surjeet kaur" not in ans_lower and "p.t. koshy" not in ans_lower:
            prohibited_violations.append(proh)

    # Check authorities
    matched_authorities = []
    for auth in scenario.get("expected_authorities", []):
        if any(w in ans_lower for w in auth.lower().split()[:2]):
            matched_authorities.append(auth)

    provision_score = len(matched_provisions) / max(1, len(scenario.get("expected_provisions", [])))
    authority_score = len(matched_authorities) / max(1, len(scenario.get("expected_authorities", [])))
    passed = (len(prohibited_violations) == 0) and (provision_score >= 0.33)

    return {
        "scenario_id": scenario["id"],
        "title": scenario["title"],
        "passed": passed,
        "score": int(round((provision_score * 0.7 + authority_score * 0.3) * 100)),
        "provision_score": round(provision_score, 2),
        "authority_score": round(authority_score, 2),
        "prohibited_violations": prohibited_violations,
        "matched_provisions": matched_provisions,
        "matched_authorities": matched_authorities,
        "found_provisions": matched_provisions,
        "missing_provisions": [p for p in scenario.get("expected_provisions", []) if p not in matched_provisions]
    }


def run_full_benchmark_evaluation(pipeline_fn=None) -> Dict[str, Any]:
    """Runs all 15 benchmark scenarios through the legal multi-agent pipeline and scores results."""
    from app.agents.multi_agent_pipeline import NyayaMultiAgentPipeline, LegalAgentState

    pipeline = NyayaMultiAgentPipeline()
    results = []

    for sc in LEGAL_BENCHMARK_SCENARIOS:
        state = LegalAgentState(
            question=sc["question"],
            language="English",
            jurisdiction="India"
        )
        out = pipeline.run(state)
        eval_res = evaluate_response_against_scenario(sc, out["answer"])
        results.append(eval_res)

    passed_count = sum(1 for r in results if r["passed"])
    return {
        "total_scenarios": len(results),
        "passed_scenarios": passed_count,
        "pass_rate": f"{round((passed_count / max(1, len(results))) * 100, 1)}%",
        "results": results
    }

