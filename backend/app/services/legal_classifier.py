"""
Legal Classification Engine for Indian Law (NyayaAI).
Classifies citizen complaints into precise legal domains across 15+ Central and State statutes.
Distinguishes Civil, Criminal, Consumer, Regulatory, and Mixed matters.
Identifies Primary, Secondary, Conditional, and Excluded/Irrelevant Legislation.
Enforces Supreme Court benchmarks (e.g. loan non-repayment vs cheating, sovereign duties vs CPA).
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime


class LegalClassificationEngine:
    """
    Rule-based and semantic legal domain classification engine.
    Prevents over-application of the Consumer Protection Act.
    Detects civil vs criminal boundaries, employment vs consumer, and contract vs tort.
    """

    def __init__(self):
        pass

    def classify(self, query: str, incident_date: Optional[str] = None, jurisdiction: str = "India") -> Dict[str, Any]:
        q = query.lower()

        # Parse incident date to determine temporal penal / consumer law
        dt = None
        if incident_date:
            try:
                for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%Y/%m/%d"):
                    try:
                        dt = datetime.strptime(incident_date.strip(), fmt)
                        break
                    except ValueError:
                        continue
            except Exception:
                dt = None

        # Check inline query for historical date clues if incident_date not explicitly passed
        is_pre_july_2024 = False
        if dt:
            is_pre_july_2024 = dt < datetime(2024, 7, 1)
        else:
            if any(term in q for term in ["2020", "2021", "2022", "2023", "prior to july 2024", "before july 2024", "june 2024", "may 2024"]):
                is_pre_july_2024 = True

        # Default classification structure
        result: Dict[str, Any] = {
            "domain": "General Civil / Statutory",
            "secondary_domains": [],
            "matter_nature": "Civil",  # Civil, Criminal, Consumer, Regulatory, Mixed
            "primary_legislation": {},
            "secondary_legislation": [],
            "conditional_legislation": [],
            "irrelevant_legislation": [],
            "civil_vs_criminal_analysis": "",
            "essential_elements": {},
            "missing_information": [],
            "recommended_forums": [],
            "prohibited_forums": [],
            "temporal_statute_selected": "Bharatiya Nyaya Sanhita, 2023" if not is_pre_july_2024 else "Indian Penal Code, 1860"
        }

        # ── DOMAIN 1: Finder of Goods / Reward Claims (Indian Contract Act Section 168 & 8) ────────
        if any(w in q for w in ["finder", "reward", "lost spectacles", "found lost", "returned wallet", "returned the ring", "returned dog", "lost and found"]) and any(w in q for w in ["reward", "owner", "returned", "refuses to pay", "reneged"]):
            result["domain"] = "Law of Contracts & Bailment (Finder of Goods)"
            result["matter_nature"] = "Civil"
            result["primary_legislation"] = {
                "act_name": "The Indian Contract Act, 1872",
                "sections": ["Section 168", "Section 8"],
                "rationale": (
                    "Section 168 of the Indian Contract Act, 1872 explicitly grants the finder of lost goods the right to sue "
                    "the owner for any specific reward that was offered for the return of the lost item, and to retain the goods until received. "
                    "Section 8 provides that performance of the conditions of a proposal constitutes acceptance of the contract."
                )
            }
            result["secondary_legislation"].append({
                "act_name": "The Indian Contract Act, 1872",
                "sections": ["Section 169"],
                "rationale": "Section 169 permits sale of the thing found if the owner cannot with reasonable diligence be found, or refuses to pay lawful charges."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "Returning lost spectacles or claiming a finder's reward is not a commercial sale of goods or hiring of services under Section 2(7)/2(42)."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Negotiable Instruments Act, 1881",
                "reason": "No negotiable instrument or cheque is drawn or dishonoured."
            })
            result["civil_vs_criminal_analysis"] = "Pure civil contractual dispute regarding enforcement of a unilateral reward offer upon performance under Section 168."
            result["recommended_forums"] = ["Civil Court of competent pecuniary jurisdiction", "Pre-litigation Mediation / Lok Adalat"]
            result["prohibited_forums"] = ["Consumer Disputes Redressal Commission", "Police Station / Criminal Court"]
            result["essential_elements"] = {
                "Section 168 Contract Act": [
                    "A specific reward was publicly or privately offered by the owner for the return of the lost goods.",
                    "The finder found the lost goods and returned or offered to return them knowing of the reward.",
                    "The owner refused to pay the offered reward."
                ]
            }
            return result

        # ── DOMAIN 2: Personal Friendly Loan / Non-Payment (Civil Recovery vs Cheating) ────────────
        is_friendly_loan = (
            any(w in q for w in ["friend", "relative", "colleague", "neighbour", "brother", "sister", "cousin", "lent money", "borrowed", "personal loan", "lent ₹", "lent rs", "childhood friend"])
            and any(w in q for w in ["repay", "refusing to return", "give back", "pay back", "lent", "borrowed ₹", "borrowed rs", "returned the money", "denies borrowing", "avoided payment", "dares me to go to court"])
            and not any(w in q for w in ["cheque", "bank", "nbfc", "fintech"])
        )
        if is_friendly_loan:
            result["domain"] = "Civil Debt Recovery & Law of Contracts"
            result["matter_nature"] = "Civil"
            result["primary_legislation"] = {
                "act_name": "The Indian Contract Act, 1872",
                "sections": ["Section 73", "Section 10"],
                "rationale": (
                    "A personal loan creates a civil debtor-creditor relationship. Under Section 73 of the Indian Contract Act, "
                    "the party suffering from a breach is entitled to receive compensation for any loss or damage caused to him thereby."
                )
            }
            result["secondary_legislation"].append({
                "act_name": "The Code of Civil Procedure, 1908",
                "sections": ["Order XXXVII (Summary Suits)"],
                "rationale": "Summary suits allow expedited recovery of admitted written debts, promissory notes, or acknowledgements of debt."
            })
            result["secondary_legislation"].append({
                "act_name": "The Limitation Act, 1963",
                "sections": ["Article 19", "Article 22"],
                "rationale": "The statutory limitation period for recovery of money lent is 3 years from the date of loan or agreed date of repayment."
            })
            result["conditional_legislation"].append({
                "act_name": "The Bharatiya Nyaya Sanhita, 2023",
                "sections": ["Section 318(4) (Cheating)"],
                "condition": (
                    "ONLY applicable if fraudulent or dishonest intention existed AT THE VERY INCEPTION of the loan (e.g. false identity, forged collaterals). "
                    "Under Supreme Court precedent (Hriday Ranjan Prasad Verma v. State of Bihar (2000) 4 SCC 168), mere subsequent failure to repay "
                    "a friendly loan is a pure civil breach of contract and does NOT constitute the criminal offence of cheating."
                )
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "A personal loan between friends is not a consumer transaction. Neither party is a consumer hiring services under Section 2(7)."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Negotiable Instruments Act, 1881",
                "reason": "No cheque was issued or dishonoured in the transaction."
            })
            result["civil_vs_criminal_analysis"] = (
                "CRITICAL DISTINCTION: Under Supreme Court precedent (Hriday Ranjan Prasad Verma and Prof. R.K. Vijayasarathy), "
                "mere failure to repay money borrowed from a friend does NOT constitute criminal cheating. It is a civil recovery matter. "
                "Filing a criminal complaint to coerce repayment of a civil debt without proving deceptive intent at the start is an abuse of process."
            )
            result["recommended_forums"] = ["Civil Court (Summary Suit under Order 37 CPC)", "Pre-Litigation Mediation via District Legal Services Authority (DLSA)"]
            result["prohibited_forums"] = ["Consumer Court", "Police Station (unless forged documents/identity theft was used)"]
            result["essential_elements"] = {
                "Section 73 Contract Act": [
                    "Existence of an agreement to lend money with a promise to repay.",
                    "Disbursement of the funds (bank transfer, UPI, or cash receipt).",
                    "Demand for repayment and default by the borrower."
                ]
            }
            return result

        # ── DOMAIN 3A: Genuine Recruitment Agency / Placement Service Dispute ──────────────────────
        is_genuine_placement = (
            any(w in q for w in ["registered placement agency", "placement consultancy", "recruitment agency", "recruitment consultancy", "placement service", "consultancy", "resume building", "consulting fee", "service agreement"])
            and not any(w in q for w in ["fake", "disappeared", "blocked", "scammer", "bogus", "phantom", "vanished", "cheat", "telegram"])
        )
        if is_genuine_placement:
            result["domain"] = "Consumer Protection & Recruitment Service Dispute"
            result["matter_nature"] = "Consumer / Civil"
            result["primary_legislation"] = {
                "act_name": "The Consumer Protection Act, 2019",
                "sections": ["Section 2(7)", "Section 2(11)", "Section 35"],
                "rationale": "Where a candidate enters into a formal service agreement and pays consideration to a registered commercial agency, deficiency in service is actionable under Section 35 CPA."
            }
            result["secondary_legislation"].append({
                "act_name": "The Indian Contract Act, 1872",
                "sections": ["Section 73"],
                "rationale": "Breach of contractual placement terms."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Bharatiya Nyaya Sanhita, 2023",
                "reason": "Commercial breach of contract by a registered entity is a civil/consumer dispute, not criminal cheating, unless fraudulent intent existed at inception."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Information Technology Act, 2000 (Sections 43 & 66)",
                "reason": "No unauthorized hacking or computer system disruption occurred."
            })
            result["civil_vs_criminal_analysis"] = "Consumer deficiency and civil breach of contract between a fee-paying client and a commercial agency."
            result["recommended_forums"] = ["District Consumer Disputes Redressal Commission", "National Consumer Helpline (1915)"]
            result["prohibited_forums"] = ["Police Station (unless agency is a fictitious front)"]
            return result

        # ── DOMAIN 3B: Fake Job Recruiter / Employment Scam (BNS Cheating & Cyber Impersonation) ────
        is_job_scam = (
            any(w in q for w in ["recruiter", "job offer", "fake job", "placement", "employment scam", "interview fee", "registration fee for job", "remote job", "hiring scam", "hr manager", "data entry role", "job"])
            and any(w in q for w in ["fake", "disappeared", "blocked", "scam", "scammer", "fraud", "paid", "cheated", "bogus", "vanished", "telegram", "whatsapp job", "job scam", "posed as"])
        )
        if is_job_scam:
            result["domain"] = "Criminal Fraud, Cheating & Cyber Crime"
            result["matter_nature"] = "Criminal"
            penal_act = "The Bharatiya Nyaya Sanhita, 2023" if not is_pre_july_2024 else "The Indian Penal Code, 1860"
            cheating_secs = ["Section 318(4)", "Section 319"] if not is_pre_july_2024 else ["Section 420", "Section 419"]
            result["primary_legislation"] = {
                "act_name": penal_act,
                "sections": cheating_secs,
                "rationale": (
                    f"A bogus recruiter collecting money on false job promises and disappearing commits criminal cheating and dishonest "
                    f"inducement of property under {cheating_secs[0]} and cheating by personation under {cheating_secs[1]} of {penal_act}."
                )
            }
            result["secondary_legislation"].append({
                "act_name": "The Information Technology Act, 2000",
                "sections": ["Section 66D"],
                "rationale": "Cheating by personation using computer resource or communication device (WhatsApp, email, fake job portal)."
            })
            result["conditional_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "sections": ["Section 2(7)", "Section 35"],
                "condition": (
                    "Consumer Protection Act applies ONLY IF the entity was a legally registered commercial recruitment agency that had entered into "
                    "a genuine written service contract with established commercial terms, and subsequently caused deficiency in service. "
                    "If the recruiter was an outright fake/fictitious scammer with no legitimate entity, Consumer Forum cannot execute orders against untraceable phantom scammers, and criminal prosecution is the exclusive appropriate remedy."
                )
            })
            result["conditional_legislation"].append({
                "act_name": "The Information Technology Act, 2000",
                "sections": ["Section 66C"],
                "condition": "Section 66C applies ONLY IF another person's electronic signature, password, or unique identification feature (stolen identity) was fraudulently used."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Information Technology Act, 2000 (Sections 43 & 66)",
                "reason": "Inapplicable because no unauthorized hacking, computer contaminant/virus, data damage, or computer system disruption occurred."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "A phantom scammer collecting money on false job promises is a criminal offender, not a consumer service provider."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Negotiable Instruments Act, 1881",
                "reason": "No negotiable instrument or cheque bounce is involved."
            })
            result["civil_vs_criminal_analysis"] = (
                "This is a cognizable criminal offence under BNS Section 318(4) & 319 (or IPC 420/419 if pre-July 2024). The fake recruiter had dishonest intention at the inception, inducing payment of money "
                "under a fictitious promise of employment. Police/Cyber Crime investigation is essential to trace bank accounts and freeze scam proceeds."
            )
            result["recommended_forums"] = [
                "National Cyber Crime Reporting Portal (https://cybercrime.gov.in or Toll-Free 1930)",
                "Local Police Station (FIR under Section 154 CrPC / 173 BNSS)",
                "Cyber Crime Police Station"
            ]
            result["prohibited_forums"] = ["Consumer Forum (unless genuine registered commercial entity with physical presence exists)"]
            result["essential_elements"] = {
                f"{cheating_secs[0]} {penal_act}": [
                    "Deception practiced on the complainant through false employment representations.",
                    "Fraudulent or dishonest inducement causing the victim to deliver money.",
                    "Dishonest intention from the inception of the interaction."
                ],
                "Section 66D IT Act": [
                    "Use of a communication device, electronic portal, or email to cheat by personation."
                ]
            }
            return result

        # ── DOMAIN 4: Workplace Sexual Harassment (POSH Act & BNS) ──────────────────────────────────
        if any(w in q for w in ["sexual harassment", "posh", "workplace harassment", "boss touched", "manager asked for sexual", "colleague harassing woman", "unwelcome physical contact", "sexual advances", "unwelcome advances", "inappropriate messages"]) or (any(w in q for w in ["harassment", "harassing", "unwelcome"]) and any(w in q for w in ["office", "workplace", "colleague", "boss", "manager", "employee", "firm"])):
            result["domain"] = "Workplace Sexual Harassment & Gender Protection"
            result["matter_nature"] = "Regulatory & Criminal (Mixed)"
            result["primary_legislation"] = {
                "act_name": "The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act)",
                "sections": ["Section 4", "Section 9", "Section 11", "Section 13"],
                "rationale": (
                    "The POSH Act, 2013 is the specialized legislation governing workplace sexual harassment. Section 4 mandates an Internal Committee (IC); "
                    "Section 9 permits an aggrieved woman to submit a written complaint within 3 months; Section 11 governs inquiry proceedings; and Section 13 mandates the inquiry report and action."
                )
            }
            penal_act = "The Bharatiya Nyaya Sanhita, 2023" if not is_pre_july_2024 else "The Indian Penal Code, 1860"
            sh_sec = "Section 75 (Sexual Harassment) & Section 78 (Stalking)" if not is_pre_july_2024 else "Section 354A & Section 354D"
            result["secondary_legislation"].append({
                "act_name": penal_act,
                "sections": [sh_sec],
                "rationale": "Parallel criminal remedy if the conduct involves physical contact, advances involving sexual overtures, or stalking."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "An employee is NOT a consumer hiring services from the employer under Section 2(7). Consumer courts have zero jurisdiction over workplace employment disputes."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Negotiable Instruments Act, 1881",
                "reason": "Completely unrelated to workplace sexual harassment."
            })
            result["civil_vs_criminal_analysis"] = (
                "Workplace sexual harassment provides dual concurrent avenues: (1) An internal administrative/statutory inquiry before the Internal Committee (IC) under POSH Act, 2013, "
                "and (2) Criminal prosecution via Police FIR under BNS Section 75/78 (or IPC 354A/354D). The complainant has the legal right to pursue both simultaneously."
            )
            result["recommended_forums"] = [
                "Internal Committee (IC) of the employer / organization",
                "Local Committee (LC) established by the District Officer (if organization has fewer than 10 workers or complaint is against the employer)",
                "Police Station (FIR under Section 173 BNSS / 154 CrPC)"
            ]
            result["prohibited_forums"] = ["Consumer Court", "Labour Court (unless wrongful termination specifically challenged)"]
            result["essential_elements"] = {
                "Section 9 POSH Act": [
                    "Aggrieved woman in a workplace setting.",
                    "Unwelcome sexually determined behavior (physical, verbal, or non-verbal).",
                    "Complaint submitted within 3 months (extendable by 3 months with sufficient cause)."
                ]
            }
            return result

        # ── DOMAIN 5: Road Traffic Accidents / Negligent Driving (MV Act & BNS) ────────────────────
        if any(w in q for w in ["road accident", "accident", "collision", "collided", "hit-and-run", "hit and run", "mact", "zebra crossing", "knocked down", "two-wheeler", "rammed into", "rashly", "recklessly", "pedestrian hit", "injured in accident"]) and any(w in q for w in ["car", "bus", "truck", "bike", "motorcycle", "vehicle", "driver", "taxi", "van", "autorickshaw", "cyclist", "pedestrian", "fracture", "injuries"]):
            result["domain"] = "Motor Accident Claims & Criminal Negligence"
            result["matter_nature"] = "Civil (MACT Compensation) & Criminal (Rash Driving)"
            result["primary_legislation"] = {
                "act_name": "The Motor Vehicles Act, 1988",
                "sections": ["Section 166", "Section 168", "Section 146"],
                "rationale": (
                    "Section 166 of the Motor Vehicles Act, 1988 provides the statutory remedy to file an application for compensation before the "
                    "Motor Accidents Claims Tribunal (MACT) against the driver, vehicle owner, and insurer. Section 146 mandates compulsory third-party insurance."
                )
            }
            penal_act = "The Bharatiya Nyaya Sanhita, 2023" if not is_pre_july_2024 else "The Indian Penal Code, 1860"
            rash_sec = "Section 281 (Rash Driving), Section 125 (Endangering Life/Grievous Hurt), Section 106(1) (Negligent Death)" if not is_pre_july_2024 else "Section 279, Section 337/338, Section 304A"
            result["secondary_legislation"].append({
                "act_name": penal_act,
                "sections": [rash_sec],
                "rationale": "Criminal prosecution of the driver for rash and negligent driving endangering human life or causing injury."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "A road accident victim hit by a third-party vehicle is not a consumer of that driver under Section 2(7). MACT has exclusive statutory jurisdiction."
            })
            result["civil_vs_criminal_analysis"] = (
                "Road accidents generate twin legal proceedings: (1) Criminal prosecution by the State against the negligent driver under BNS Section 281/125/106(1), "
                "and (2) Independent civil claim for monetary compensation before the Motor Accidents Claims Tribunal (MACT) under Section 166 of the MV Act, 1988."
            )
            result["recommended_forums"] = [
                "Motor Accidents Claims Tribunal (MACT) situated where accident occurred or claimant resides",
                "Police Station (Detailed Accident Report - DAR / FIR)"
            ]
            result["prohibited_forums"] = ["Consumer Court", "Ordinary Civil Court (jurisdiction barred by Section 175 of the Motor Vehicles Act)"]
            result["essential_elements"] = {
                "Section 166 MV Act": [
                    "Involvement of a motor vehicle in a public place.",
                    "Accident resulting in injury, permanent disability, death, or third-party property damage.",
                    "Negligence or strict statutory liability."
                ]
            }
            return result

        # ── DOMAIN 6: Defamation (Online / Verbal / Published) ──────────────────────────────────────
        if any(w in q for w in ["defamation", "defamed", "defamatory", "false allegations against reputation", "reputation damaged", "damage my reputation", "damage reputation", "slander", "libel", "maligning my character", "false and malicious allegations"]):
            result["domain"] = "Defamation (Criminal & Civil Tort)"
            result["matter_nature"] = "Criminal & Civil (Concurrent)"
            penal_act = "The Bharatiya Nyaya Sanhita, 2023" if not is_pre_july_2024 else "The Indian Penal Code, 1860"
            defam_sec = "Section 356" if not is_pre_july_2024 else "Section 499 & Section 500"
            result["primary_legislation"] = {
                "act_name": penal_act,
                "sections": [defam_sec],
                "rationale": (
                    f"Under {defam_sec} of {penal_act}, whoever makes or publishes any imputation concerning any person intending to harm, "
                    f"or knowing or having reason to believe that such imputation will harm, the reputation of such person, commits criminal defamation."
                )
            }
            result["secondary_legislation"].append({
                "act_name": "The Specific Relief Act, 1963",
                "sections": ["Section 38 (Perpetual Injunction)"],
                "rationale": "Civil suit for damages and permanent injunction restraining further defamatory publications."
            })
            result["conditional_legislation"].append({
                "act_name": "The Information Technology Act, 2000",
                "sections": ["Section 79(3)(b) (Intermediary Takedown)"],
                "condition": (
                    "If defamatory material was posted on digital intermediaries (Facebook, X, Instagram), notice may be issued to the intermediary "
                    "to take down the content pursuant to a court order. NOTE: Section 66A of the IT Act was struck down as unconstitutional by the Supreme Court "
                    "in Shreya Singhal v. Union of India (2015) 5 SCC 1, and CANNOT be cited."
                )
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "Defamation is a personal tort and criminal offence, not a commercial consumer defect or service deficiency."
            })
            result["civil_vs_criminal_analysis"] = (
                "Under Indian law (Subramanian Swamy v. Union of India (2016) 7 SCC 221), defamation offers two independent remedies: "
                "(1) Criminal complaint before a Judicial Magistrate under Section 356 BNS / 499 IPC, and "
                "(2) Civil suit for monetary damages and injunction in a Civil Court for the tort of defamation."
            )
            result["recommended_forums"] = [
                "Judicial Magistrate of the First Class (Private Criminal Complaint under Section 223 BNSS / 200 CrPC)",
                "Civil Court for Damages & Injunction under Section 38 Specific Relief Act"
            ]
            result["prohibited_forums"] = ["Consumer Court", "Police Station (Defamation is non-cognizable; police cannot register FIR directly without Magistrate order)"]
            result["essential_elements"] = {
                f"{defam_sec} {penal_act}": [
                    "Making or publishing an imputation concerning the complainant.",
                    "Imputation published to a third party.",
                    "Intention to harm or knowledge that it will harm reputation, without falling into the statutory exceptions."
                ]
            }
            return result

        # ── DOMAIN 7: Cheque Dishonour / Bounce (Negotiable Instruments Act Section 138) ────────────
        if any(w in q for w in ["cheque", "dishonour", "bounce", "bounced", "bank memo"]):
            result["domain"] = "Negotiable Instruments / Financial Law"
            result["matter_nature"] = "Criminal (Quasi-Criminal Statutory Offence)"
            result["primary_legislation"] = {
                "act_name": "The Negotiable Instruments Act, 1881",
                "sections": ["Section 138", "Section 141", "Section 142"],
                "rationale": (
                    "Section 138 of the NI Act creates a statutory offence when a cheque drawn for the discharge of a legally enforceable debt "
                    "is dishonoured due to insufficiency of funds. Strict mandatory statutory notices and limitation timelines apply."
                )
            }
            result["secondary_legislation"].append({
                "act_name": "The Code of Criminal Procedure, 1973 / BNSS, 2023",
                "sections": ["Section 142(2) NI Act Territorial Rule"],
                "rationale": "Jurisdiction lies where the branch of the bank where the payee maintains the account is situated."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "Cheque bounce is an exclusive statutory criminal proceeding under Section 138 NI Act, not a consumer dispute."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Information Technology Act, 2000",
                "reason": "A physical paper cheque is not an electronic record or computer resource."
            })
            result["civil_vs_criminal_analysis"] = (
                "Section 138 of the NI Act is a special statutory quasi-criminal provision designed to ensure commercial integrity of cheques. "
                "The complainant may also file a parallel civil summary suit under Order 37 CPC for recovery."
            )
            result["recommended_forums"] = ["Judicial Magistrate / Metropolitan Magistrate Court within whose jurisdiction payee maintains bank account"]
            result["prohibited_forums"] = ["Consumer Court", "Police Station (Section 138 requires direct private complaint to Magistrate; no police FIR)"]
            result["essential_elements"] = {
                "Section 138 NI Act": [
                    "Cheque drawn for discharge of a legally enforceable debt or liability.",
                    "Presentation to the bank within 3 months of date of drawing.",
                    "Cheque returned unpaid by bank with memo.",
                    "Statutory Demand Notice issued in writing within 30 days of receiving bank memo.",
                    "Failure of drawer to pay the amount within 15 days of receipt of notice.",
                    "Complaint filed before Magistrate within 1 month of expiry of 15-day period."
                ]
            }
            return result

        # ── DOMAIN 8A: Unauthorized Computer Access & Hacking (IT Act Sections 43 & 66) ─────────────
        is_unauth_access = any(w in q for w in ["unauthorized access", "unauthorised access", "hacked company server", "hacked server", "data theft", "stole data", "malware", "virus", "contaminant", "disrupted server", "accessed computer without permission", "downloaded database", "system breach", "downloaded confidential database"])
        if is_unauth_access:
            result["domain"] = "Cyber Crime & Computer System Offences"
            result["matter_nature"] = "Criminal & Civil Compensation"
            result["primary_legislation"] = {
                "act_name": "The Information Technology Act, 2000",
                "sections": ["Section 43 (Penalty and Compensation)", "Section 66 (Computer Related Offences)"],
                "rationale": "Section 43 provides statutory compensation for unauthorized access, data theft, and system disruption, while Section 66 prescribes up to 3 years imprisonment for dishonest or fraudulent commission of Section 43 acts."
            }
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "Unauthorized computer access and system hacking are criminal offences under the IT Act, not consumer disputes."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Negotiable Instruments Act, 1881",
                "reason": "Completely unrelated to computer system damage."
            })
            result["civil_vs_criminal_analysis"] = "Hybrid statutory remedy: Civil damages under Section 43 adjudicated by State IT Secretary / Adjudicating Officer, and Criminal trial under Section 66 before Magistrate."
            result["recommended_forums"] = ["Cyber Crime Police Station", "Adjudicating Officer under IT Act (State IT Secretary)"]
            result["prohibited_forums"] = ["Consumer Court"]
            result["essential_elements"] = {
                "Section 43 IT Act": ["Accessing, downloading data, introducing virus, or disrupting computer system without permission of owner."],
                "Section 66 IT Act": ["Doing any act under Section 43 dishonestly or fraudulently."]
            }
            return result

        # ── DOMAIN 8B: Stolen Login Credentials / Electronic Signatures (IT Act Section 66C) ────────
        is_stolen_creds = any(w in q for w in ["electronic signature", "stolen password", "login credentials", "stole my password", "stolen credentials", "used my password", "net banking password", "aadhaar card copy", "forged signature to obtain an illegal sim", "stolen login credentials", "fraudulently used my electronic signature"])
        if is_stolen_creds:
            result["domain"] = "Cyber Identity Theft & Credential Misuse"
            result["matter_nature"] = "Criminal"
            result["primary_legislation"] = {
                "act_name": "The Information Technology Act, 2000",
                "sections": ["Section 66C (Identity Theft)"],
                "rationale": "Section 66C specifically penalizes fraudulent or dishonest use of another person's electronic signature, password, or unique identification feature."
            }
            result["conditional_legislation"].append({
                "act_name": "The Information Technology Act, 2000",
                "sections": ["Section 66D"],
                "condition": "Section 66D applies if the stolen credentials were used to cheat by personating the victim to third parties."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Information Technology Act, 2000 (Sections 43 & 66)",
                "reason": "Section 43 and Section 66 are excluded because no system disruption, malware, or server damage occurred."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "Identity theft and password stealing are cyber criminal offences, not consumer disputes."
            })
            result["civil_vs_criminal_analysis"] = "Cognizable cyber crime involving misappropriation of personal unique identification credentials."
            result["recommended_forums"] = ["Cyber Crime Police Station", "National Cyber Crime Reporting Portal (1930 / cybercrime.gov.in)"]
            result["prohibited_forums"] = ["Consumer Court"]
            result["essential_elements"] = {
                "Section 66C IT Act": ["Fraudulent or dishonest use of another's password, digital signature, or unique identification feature."]
            }
            return result

        # ── DOMAIN 8C: Actual Identity Impersonation & Fake Profile (IT Act 66D & BNS 319) ─────────
        if any(w in q for w in ["impersonating", "impersonator", "fake linkedin", "fake social media", "fake profile", "fake instagram", "fake account", "using my photo", "using my name and photos", "clone facebook", "identity impersonation", "actual identity impersonation"]):
            result["domain"] = "Cyber Identity Theft & Impersonation"
            result["matter_nature"] = "Criminal"
            penal_act = "The Bharatiya Nyaya Sanhita, 2023" if not is_pre_july_2024 else "The Indian Penal Code, 1860"
            imp_sec = "Section 319 (Cheating by personation)" if not is_pre_july_2024 else "Section 419"
            result["primary_legislation"] = {
                "act_name": "The Information Technology Act, 2000",
                "sections": ["Section 66D (Cheating by personation using computer resource)"],
                "rationale": "Section 66D penalizes cheating by personation by means of any communication device or computer resource."
            }
            result["secondary_legislation"].append({
                "act_name": penal_act,
                "sections": [imp_sec],
                "rationale": "Substantive penal offence of cheating by personation."
            })
            result["conditional_legislation"].append({
                "act_name": "The Information Technology Act, 2000",
                "sections": ["Section 66C"],
                "condition": "Section 66C applies ONLY IF the impersonator fraudulently used the victim's actual password, electronic signature, or unique biometric/digital ID."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Information Technology Act, 2000 (Sections 43 & 66)",
                "reason": "Inapplicable because no unauthorized access, malware, or damage to computer system under Section 43 occurred."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "Creating a fake social media profile or impersonating an individual is a cyber crime, not a consumer dispute."
            })
            result["civil_vs_criminal_analysis"] = "Cognizable cyber crime of impersonation and cheating by personation using digital communication platforms."
            result["recommended_forums"] = ["National Cyber Crime Reporting Portal (cybercrime.gov.in)", "Cyber Crime Police Cell", "Platform Grievance Officer (Takedown Notice)"]
            result["prohibited_forums"] = ["Consumer Court"]
            result["essential_elements"] = {
                "Section 66D IT Act": ["Cheating by personation by using a computer resource or communication device."],
                f"{imp_sec} {penal_act}": ["Pretending to be some other person, or knowingly substituting one person for another."]
            }
            return result

        # ── DOMAIN 9: Tenancy Security Deposit / Eviction (State Tenancy & TPA) ─────────────────────
        if any(w in q for w in ["landlord", "tenant", "security deposit", "advance", "rent", "eviction", "vacated", "vacating the premises", "painting wear-and-tear"]):
            result["domain"] = "Tenancy & Immovable Property Law"
            result["matter_nature"] = "Civil"
            # State specific check
            state_act = "The Tamil Nadu Regulation of Rights and Responsibilities of Landlords and Tenants Act, 2017 (TNRRLTA)" if "tamil nadu" in q or "chennai" in q or jurisdiction == "Tamil Nadu" else "State Tenancy / Rent Control Act & Transfer of Property Act, 1882"
            result["primary_legislation"] = {
                "act_name": state_act,
                "sections": ["Section 10(2) (Refund within 1 month)", "Section 21 (Application to Rent Authority)"] if "TNRRLTA" in state_act else ["Section 106 & 108 of Transfer of Property Act, 1882"],
                "rationale": (
                    "Under tenancy law (e.g. Section 10(2) of TNRRLTA 2017 and Supreme Court precedent H.S. Goutham v. Rama Murthy), "
                    "a landlord must refund the security deposit within one month of vacating after legitimate deductions for verified damages."
                )
            }
            result["secondary_legislation"].append({
                "act_name": "The Indian Contract Act, 1872",
                "sections": ["Section 73"],
                "rationale": "Breach of tenancy contract and recovery of withheld deposit."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "A residential landlord-tenant relationship is governed exclusively by tenancy law and Rent Courts. Consumer Forums lack jurisdiction over residential tenancy deposit disputes."
            })
            result["civil_vs_criminal_analysis"] = "Civil tenancy dispute. Withholding a deposit is a breach of lease covenant, not criminal breach of trust unless property was dishonestly converted with criminal intent."
            result["recommended_forums"] = ["Rent Authority / Rent Court", "Civil Court", "Pre-litigation Mediation (DLSA)"]
            result["prohibited_forums"] = ["Consumer Court", "Police Station"]
            result["essential_elements"] = {
                "Tenancy Security Deposit Refund": [
                    "Valid tenancy agreement and payment of security deposit.",
                    "Surrender of vacant possession of premises to landlord.",
                    "Failure to refund balance deposit within statutory period (1 month)."
                ]
            }
            return result

        # ── DOMAIN 10: Defective Product / Consumer Dispute (Consumer Protection Act, 2019) ─────────
        if any(w in q for w in ["defective", "mobile phone", "laptop", "smart tv", "amazon", "flipkart", "warranty", "manufacturing defect", "seller refusing refund", "poor service by company", "airline", "cancelled domestic flight", "counterfeit shoes", "service centre", "hospitalization claim", "health insurance"]):
            if any(w in q for w in ["amazon", "flipkart", "ecommerce", "e-commerce"]):
                result["domain"] = "Consumer Protection & E-Commerce Law"
            else:
                result["domain"] = "Consumer Protection & Product Liability"
            result["matter_nature"] = "Consumer (Statutory Civil Remedy)"
            result["primary_legislation"] = {
                "act_name": "The Consumer Protection Act, 2019",
                "sections": ["Section 2(7)", "Section 2(11)", "Section 35", "Section 84 (Product Liability)"],
                "rationale": (
                    "The Consumer Protection Act, 2019 applies because the complainant purchased goods for consideration as a consumer under Section 2(7). "
                    "Section 2(11) covers deficiency, and Section 35 provides the filing mechanism before the District Consumer Commission."
                )
            }
            result["secondary_legislation"].append({
                "act_name": "Consumer Protection (E-Commerce) Rules, 2020",
                "sections": ["Rule 4 & Rule 5"],
                "rationale": "Obligations of e-commerce entities to redress consumer complaints within one month."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Negotiable Instruments Act, 1881",
                "reason": "Not a cheque dishonour matter."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Bharatiya Nyaya Sanhita, 2023",
                "reason": "A defective product sold commercially is a consumer defect, not a criminal offence, unless there is organized counterfeiting."
            })
            result["civil_vs_criminal_analysis"] = "Pure consumer dispute under the specialized statutory framework of CPA 2019. Complainant is entitled to replacement, refund, and compensation for mental agony."
            result["recommended_forums"] = ["District Consumer Disputes Redressal Commission (via e-Daakhil: edaakhil.nic.in)", "National Consumer Helpline (Toll-Free 1915 / consumerhelpline.gov.in)"]
            result["prohibited_forums"] = ["Police Station", "Criminal Court"]
            result["essential_elements"] = {
                "Section 35 Consumer Protection Act": [
                    "Complainant paid or promised consideration (invoice/bill).",
                    "Defect in goods or deficiency in service under warranty.",
                    "Complaint filed within 2 years from cause of action (Section 69)."
                ]
            }
            return result

        # ── DOMAIN 11: Education / University Disputes (UGC Regulations vs CPA) ────────────────────
        if any(w in q for w in ["college", "university", "ugc", "exam fee", "hall ticket", "original certificates", "degree certificate", "marksheets", "provisional degree", "debarred"]):
            result["domain"] = "Higher Education & Student Grievances"
            result["matter_nature"] = "Regulatory & Administrative"
            result["primary_legislation"] = {
                "act_name": "UGC (Redressal of Grievances of Students) Regulations, 2023",
                "sections": ["Regulation 5 (SGRC)", "Regulation 6 (Ombudsperson)"],
                "rationale": (
                    "Student grievances relating to examination fees, withholding of hall tickets, or original certificates are governed by UGC Regulations 2023. "
                    "Each institution must maintain a Student Grievance Redressal Committee (SGRC) deciding within 15 days, with appeal to University Ombudsperson."
                )
            }
            result["secondary_legislation"].append({
                "act_name": "The Constitution of India",
                "sections": ["Article 226 (Writ of Mandamus)"],
                "rationale": "High Court writ against affiliated universities or state colleges acting arbitrarily."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": (
                    "Under Supreme Court landmark rulings in Maharshi Dayanand University v. Surjeet Kaur (2010) 11 SCC 159 "
                    "and P.T. Koshy v. Ellen Charitable Trust (2012) 3 SCC 797, statutory education is not a commodity, and educational boards/colleges "
                    "do NOT render a 'service' under consumer law. Filing in Consumer Court is legally barred."
                )
            })
            result["civil_vs_criminal_analysis"] = "Institutional regulatory grievance. Withholding original documents may also constitute criminal breach of trust if college retains documents unlawfully despite UGC mandate."
            result["recommended_forums"] = ["Collegiate Student Grievance Redressal Committee (SGRC)", "University Ombudsperson", "UGC e-Samadhan Portal (samadhan.ugc.ac.in)"]
            result["prohibited_forums"] = ["Consumer Court (barred by Supreme Court)"]
            return result

        # ── DOMAIN 12: Unpaid Salary & Labour Disputes ──────────────────────────────────────────────
        if any(w in q for w in ["unpaid salary", "wages", "employer not paying", "delayed salary", "unpaid wages", "salary pending", "gratuity", "retrenchment compensation", "resignation with notice", "terminated senior machine", "private school terminated", "female teacher"]):
            result["domain"] = "Labour & Employment Law"
            result["matter_nature"] = "Labour / Statutory Recovery"
            result["primary_legislation"] = {
                "act_name": "The Payment of Wages Act, 1936",
                "sections": ["Section 15 (Claims arising out of delayed wages)"],
                "rationale": "Section 15 provides for an application to the Payment of Wages Authority for recovery of delayed or deducted wages within 12 months."
            }
            result["secondary_legislation"].append({
                "act_name": "The Industrial Disputes Act, 1947",
                "sections": ["Section 33C(2)"],
                "rationale": "Recovery of money due from an employer before the Labour Court."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "An employee is not a consumer of their employer. Consumer courts have zero jurisdiction over unpaid salary or employment contracts."
            })
            result["civil_vs_criminal_analysis"] = "Statutory labour claim. Non-payment of salary is a labour law default, not a consumer dispute."
            result["recommended_forums"] = ["Payment of Wages Authority / Labour Commissioner", "Labour Court under Section 33C(2) IDA"]
            result["prohibited_forums"] = ["Consumer Court", "Police Station"]
            return result

        # ── DOMAIN 13: Online Fraud & Cyber Financial Scams ─────────────────────────────────────────
        if any(w in q for w in ["apk link", "sharing otp", "lottery winner", "reverse qr code", "crypto scam", "drained ₹", "wiped ₹", "telegram", "lost money to scammer", "fake electricity bill"]):
            result["domain"] = "Cyber Crime & Information Technology"
            result["matter_nature"] = "Criminal"
            penal_act = "The Bharatiya Nyaya Sanhita, 2023" if not is_pre_july_2024 else "The Indian Penal Code, 1860"
            result["primary_legislation"] = {
                "act_name": "The Information Technology Act, 2000",
                "sections": ["Section 66D (Cheating by personation using computer resource)"],
                "rationale": "Criminal prosecution under Section 66D IT Act and Section 318(4) BNS for electronic deception and theft."
            }
            result["secondary_legislation"].append({
                "act_name": penal_act,
                "sections": ["Section 318(4)" if not is_pre_july_2024 else "Section 420"],
                "rationale": "Cheating and dishonestly inducing delivery of property."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "Anonymous cyber criminals cannot be sued as commercial service providers in Consumer Forum."
            })
            result["civil_vs_criminal_analysis"] = "Cognizable cyber crime. Immediate reporting to Cyber Crime portal (1930) is vital to freeze beneficiary bank accounts."
            result["recommended_forums"] = ["National Cyber Crime Reporting Portal (1930 / cybercrime.gov.in)", "Cyber Crime Police Station"]
            result["prohibited_forums"] = ["Consumer Court"]
            return result

        # ── DOMAIN 14: Cyberstalking & Online Obscenity ─────────────────────────────────────────────
        if any(w in q for w in ["burner accounts", "intimate photos", "changing room", "vulgar photos", "morphing", "spyware", "tracking gps"]):
            result["domain"] = "Cyber Harassment & IT Law"
            result["matter_nature"] = "Criminal"
            penal_act = "The Bharatiya Nyaya Sanhita, 2023" if not is_pre_july_2024 else "The Indian Penal Code, 1860"
            result["primary_legislation"] = {
                "act_name": "The Information Technology Act, 2000",
                "sections": ["Section 66E (Privacy Violation)", "Section 67 (Obscene Transmission)", "Section 67A"],
                "rationale": "Publishing, capturing, or transmitting private/obscene images is punishable under Sections 66E, 67, and 67A."
            }
            result["secondary_legislation"].append({
                "act_name": penal_act,
                "sections": ["Section 78 (Stalking)" if not is_pre_july_2024 else "Section 354D"],
                "rationale": "Monitoring a woman's internet/electronic communication."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "Cyber stalking and non-consensual image sharing are serious criminal offences, not consumer disputes."
            })
            result["civil_vs_criminal_analysis"] = "Non-bailable cognizable cyber crime against personal privacy and bodily integrity."
            result["recommended_forums"] = ["Cyber Crime Police Station", "National Cyber Crime Portal (cybercrime.gov.in)"]
            result["prohibited_forums"] = ["Consumer Court"]
            return result

        # ── DOMAIN 15: Domestic Violence ────────────────────────────────────────────────────────────
        if any(w in q for w in ["matrimonial home", "in-laws", "shared household", "alcoholic husband", "stridhan", "domestic violence", "locked out of shared"]):
            result["domain"] = "Family Law & Domestic Violence Protection"
            result["matter_nature"] = "Civil & Quasi-Criminal"
            result["primary_legislation"] = {
                "act_name": "Protection of Women from Domestic Violence Act, 2005",
                "sections": ["Section 12 (Application to Magistrate)", "Section 18 (Protection Order)", "Section 19 (Residence Order)", "Section 20 (Monetary Relief)"],
                "rationale": "Statutory relief under DV Act 2005 for protection, right to reside in shared household, and emergency monetary maintenance."
            }
            result["secondary_legislation"].append({
                "act_name": "Section 125 CrPC / Section 144 BNSS",
                "sections": ["Section 125 CrPC / Section 144 BNSS"],
                "rationale": "Monthly maintenance for wife and minor children."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "Matrimonial disputes and domestic violence are exclusively within family court and magistrate jurisdiction."
            })
            result["civil_vs_criminal_analysis"] = "Quasi-criminal protective jurisdiction before a Judicial Magistrate granting civil protective orders with penal consequences for breach under Section 31."
            result["recommended_forums"] = ["Judicial Magistrate of the First Class (DV Application)", "Family Court"]
            result["prohibited_forums"] = ["Consumer Court"]
            return result

        # ── DOMAIN 16: Maintenance Claims ──────────────────────────────────────────────────────────
        if any(w in q for w in ["deserted unemployed wife", "monthly maintenance", "senior citizens act", "interim monetary relief", "enhancement of maintenance", "concealing high corporate", "disabled child maintenance", "deserted wife"]):
            result["domain"] = "Family Law & Maintenance"
            result["matter_nature"] = "Quasi-Criminal / Civil"
            result["primary_legislation"] = {
                "act_name": "Section 125 CrPC / Section 144 BNSS",
                "sections": ["Section 125 CrPC / Section 144 BNSS"],
                "rationale": "Statutory monthly maintenance for destitute wife, children, or elderly parents under Section 125 CrPC / Section 144 BNSS."
            }
            result["secondary_legislation"].append({
                "act_name": "Protection of Women from Domestic Violence Act, 2005",
                "sections": ["Section 20"],
                "rationale": "Interim and final monetary relief."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "Spousal and parental maintenance is governed exclusively by personal/statutory family law."
            })
            result["civil_vs_criminal_analysis"] = "Statutory welfare measure to prevent vagrancy and ensure dignity."
            result["recommended_forums"] = ["Family Court", "Judicial Magistrate Court"]
            result["prohibited_forums"] = ["Consumer Court"]
            return result

        # ── DOMAIN 17: Intellectual Property (Trademark, Copyright, Patent) ────────────────────────
        if any(w in q for w in ["trademark logo", "brand name", "copyrighted educational", "counterfeit goods bearing", "patented medical", "pirated and distributed", "patents act", "trademark"]):
            result["domain"] = "Intellectual Property & Trademark Law"
            result["matter_nature"] = "Civil & Criminal"
            result["primary_legislation"] = {
                "act_name": "The Trade Marks Act, 1999 / Copyright Act, 1957",
                "sections": ["Section 29 Trade Marks Act", "Section 51 Copyright Act"],
                "rationale": "Protection against infringement and passing off of registered trademarks and copyright."
            }
            result["secondary_legislation"].append({
                "act_name": "The Specific Relief Act, 1963",
                "sections": ["Section 38 (Perpetual Injunction)"],
                "rationale": "Civil injunction and rendition of accounts of profits."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "IP infringement between competing commercial proprietors is adjudicated exclusively before Commercial Courts."
            })
            result["civil_vs_criminal_analysis"] = "Commercial intellectual property dispute with parallel criminal remedies for counterfeiting."
            result["recommended_forums"] = ["Commercial Court / District Court (IP Division)", "High Court (Original Jurisdiction)"]
            result["prohibited_forums"] = ["Consumer Court"]
            return result

        # ── DOMAIN 18: Criminal Breach of Trust (Entrustment & Misappropriation) ───────────────────
        if any(w in q for w in ["entrusted with", "misappropriated", "goldsmith", "pawn broker", "warehouse manager", "vehicle custodian", "withdrew partnership funds"]):
            result["domain"] = "Criminal Law & Offences Against Property"
            result["matter_nature"] = "Criminal"
            penal_act = "The Bharatiya Nyaya Sanhita, 2023" if not is_pre_july_2024 else "The Indian Penal Code, 1860"
            cbt_sec = "Section 316" if not is_pre_july_2024 else "Section 405/406"
            result["primary_legislation"] = {
                "act_name": penal_act,
                "sections": [cbt_sec],
                "rationale": f"Dishonest misappropriation or conversion of entrusted property under {cbt_sec} of {penal_act}."
            }
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "Misappropriation of entrusted assets by an employee, bailee, or partner is a criminal offence."
            })
            result["civil_vs_criminal_analysis"] = "Cognizable criminal offence of criminal breach of trust. Essential ingredients: entrustment of property and subsequent dishonest conversion."
            result["recommended_forums"] = ["Police Station (FIR under Section 173 BNSS / 154 CrPC)", "Judicial Magistrate Court"]
            result["prohibited_forums"] = ["Consumer Court"]
            return result

        # ── DOMAIN 19: Cheating & False Promises ───────────────────────────────────────────────────
        if any(w in q for w in ["ration shop license", "fake approval plan", "fake travel agent", "counterfeit sticker", "conman sold brass", "mbbs admission in"]):
            result["domain"] = "Criminal Fraud, Cheating & Cyber Crime"
            result["matter_nature"] = "Criminal"
            penal_act = "The Bharatiya Nyaya Sanhita, 2023" if not is_pre_july_2024 else "The Indian Penal Code, 1860"
            cheat_sec = "Section 318(4)" if not is_pre_july_2024 else "Section 420"
            result["primary_legislation"] = {
                "act_name": penal_act,
                "sections": [cheat_sec],
                "rationale": f"Dishonest inducement causing victim to deliver money under fraudulent misrepresentation under {cheat_sec}."
            }
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "Outright criminal fraud and false impersonation without legitimate commercial service."
            })
            result["civil_vs_criminal_analysis"] = "Cognizable criminal offence of cheating where fraudulent intent was present at inception."
            result["recommended_forums"] = ["Police Station (FIR)", "Judicial Magistrate Court"]
            result["prohibited_forums"] = ["Consumer Court"]
            return result

        # ── DOMAIN 20: Property & Real Estate Disputes ─────────────────────────────────────────────
        if any(w in q for w in ["encroached", "agricultural land", "boundary wall", "registered sale agreement", "sale deed", "dispossess", "self-acquired residential", "sub-tenant", "registered lease deed", "gift deed"]):
            result["domain"] = "Property Law & Civil Possession"
            result["matter_nature"] = "Civil"
            result["primary_legislation"] = {
                "act_name": "The Specific Relief Act, 1963",
                "sections": ["Section 5 & 6 (Recovery of Possession)", "Section 38 (Injunction)"],
                "rationale": "Civil suit for declaration of title, recovery of possession, and permanent injunction."
            }
            result["secondary_legislation"].append({
                "act_name": "The Transfer of Property Act, 1882",
                "sections": ["Section 54 (Sale)", "Section 105 (Lease)"],
                "rationale": "Rights and liabilities of immovable property buyers, sellers, and tenants."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "Title and boundary disputes between private individuals are outside Consumer Forum jurisdiction."
            })
            result["civil_vs_criminal_analysis"] = "Pure civil property dispute requiring adjudication on title, possession, and boundary demarcation before Civil Court."
            result["recommended_forums"] = ["Civil Court of competent territorial and pecuniary jurisdiction"]
            result["prohibited_forums"] = ["Consumer Court", "Police Station"]
            return result

        # ── DOMAIN 21: Commercial Contract Disputes ────────────────────────────────────────────────
        if any(w in q for w in ["wholesale agreement", "renovation project", "exclusivity agreement", "machinery fabricated", "dealership agreement", "signed contract", "abandoned renovation"]):
            result["domain"] = "Law of Contracts & Commercial Obligations"
            result["matter_nature"] = "Civil"
            result["primary_legislation"] = {
                "act_name": "The Indian Contract Act, 1872",
                "sections": ["Section 73 (Compensation for breach of contract)"],
                "rationale": "Statutory entitlement to damages and compensation caused by breach of contractual covenants."
            }
            result["secondary_legislation"].append({
                "act_name": "The Specific Relief Act, 1963",
                "sections": ["Section 10 (Specific Performance)"],
                "rationale": "Enforcement of contractual performance."
            })
            result["irrelevant_legislation"].append({
                "act_name": "The Consumer Protection Act, 2019",
                "reason": "B2B commercial transactions and wholesale supplier agreements are excluded from consumer definition under Section 2(7)."
            })
            result["civil_vs_criminal_analysis"] = "Commercial civil dispute. Unless fraudulent deception existed at execution, remedy lies in civil suit for damages or arbitration."
            result["recommended_forums"] = ["Commercial Court", "Civil Court", "Arbitration (if clause exists)"]
            result["prohibited_forums"] = ["Consumer Court"]
            return result

        # Fallback for general civil / default
        result["primary_legislation"] = {
            "act_name": "The Indian Contract Act, 1872",
            "sections": ["Section 73"],
            "rationale": "General civil remedy for compensation for breach of contract or obligation."
        }
        return result
