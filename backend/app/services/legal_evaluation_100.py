"""
Authoritative 100 Indian Legal Complaint Evaluation Dataset (Phase 7).
Permanent benchmark covering all 20 required domains.
Verified by legal engineering and compliance benchmarks.
"""

from typing import List, Dict, Any

LEGAL_EVALUATION_100: List[Dict[str, Any]] = [
    {
        "id": "scenario_001",
        "category": "contract",
        "complaint": "Commercial supplier failed to deliver goods after signing wholesale agreement and accepting advance.",
        "expected_legal_domain": "Contract disputes",
        "expected_primary_legislation": "The Indian Contract Act, 1872",
        "relevant_sections": [
            "Section 73"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Indian Contract Act, 1872 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_002",
        "category": "contract",
        "complaint": "Contractor abandoned renovation project halfway despite taking 80% contract payment.",
        "expected_legal_domain": "Contract disputes",
        "expected_primary_legislation": "The Indian Contract Act, 1872",
        "relevant_sections": [
            "Section 73"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Indian Contract Act, 1872 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_003",
        "category": "contract",
        "complaint": "Consulting firm breached non-disclosure and exclusivity agreement signed with client.",
        "expected_legal_domain": "Contract disputes",
        "expected_primary_legislation": "The Indian Contract Act, 1872",
        "relevant_sections": [
            "Section 73"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Indian Contract Act, 1872 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_004",
        "category": "contract",
        "complaint": "Buyer refused to accept custom-manufactured machinery fabricated under signed contract.",
        "expected_legal_domain": "Contract disputes",
        "expected_primary_legislation": "The Indian Contract Act, 1872",
        "relevant_sections": [
            "Section 73"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Indian Contract Act, 1872 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_005",
        "category": "contract",
        "complaint": "Distributor terminated dealership agreement abruptly without giving mandatory 60 days contractual notice.",
        "expected_legal_domain": "Contract disputes",
        "expected_primary_legislation": "The Indian Contract Act, 1872",
        "relevant_sections": [
            "Section 73"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Indian Contract Act, 1872 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_006",
        "category": "cheque_bounce",
        "complaint": "Client issued cheque of \u20b91,00,000 for timber purchase that got dishonoured with memo funds insufficient.",
        "expected_legal_domain": "Negotiable Instruments / Financial Law",
        "expected_primary_legislation": "The Negotiable Instruments Act, 1881",
        "relevant_sections": [
            "Section 138"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Negotiable Instruments Act, 1881 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_007",
        "category": "cheque_bounce",
        "complaint": "Debtor gave cheque of \u20b945,000 against settlement agreement which bounced due to signature mismatch and insufficient funds.",
        "expected_legal_domain": "Negotiable Instruments / Financial Law",
        "expected_primary_legislation": "The Negotiable Instruments Act, 1881",
        "relevant_sections": [
            "Section 138"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Negotiable Instruments Act, 1881 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_008",
        "category": "cheque_bounce",
        "complaint": "Cheque of \u20b92,50,000 issued for legal services rendered was returned by bank marked account closed.",
        "expected_legal_domain": "Negotiable Instruments / Financial Law",
        "expected_primary_legislation": "The Negotiable Instruments Act, 1881",
        "relevant_sections": [
            "Section 138"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Negotiable Instruments Act, 1881 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_009",
        "category": "cheque_bounce",
        "complaint": "Tenant issued cheque of \u20b950,000 for accumulated rent which dishonoured for insufficient balance.",
        "expected_legal_domain": "Negotiable Instruments / Financial Law",
        "expected_primary_legislation": "The Negotiable Instruments Act, 1881",
        "relevant_sections": [
            "Section 138"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Negotiable Instruments Act, 1881 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_010",
        "category": "cheque_bounce",
        "complaint": "Contractor received cheque of \u20b980,000 from client which was returned unpaid by bank.",
        "expected_legal_domain": "Negotiable Instruments / Financial Law",
        "expected_primary_legislation": "The Negotiable Instruments Act, 1881",
        "relevant_sections": [
            "Section 138"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Negotiable Instruments Act, 1881 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_011",
        "category": "online_fraud",
        "complaint": "Received fake electricity bill SMS with APK link that drained \u20b935,000 from my bank account.",
        "expected_legal_domain": "Cyber Crime & Information Technology",
        "expected_primary_legislation": "The Information Technology Act, 2000",
        "relevant_sections": [
            "Section 66D"
        ],
        "conditional_sections": [
            "The Consumer Protection Act, 2019 (Section 35)"
        ],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Information Technology Act, 2000 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_012",
        "category": "online_fraud",
        "complaint": "Scammer called posing as customer care agent and tricked me into sharing OTP losing \u20b920,000.",
        "expected_legal_domain": "Cyber Crime & Information Technology",
        "expected_primary_legislation": "The Information Technology Act, 2000",
        "relevant_sections": [
            "Section 66D"
        ],
        "conditional_sections": [
            "The Consumer Protection Act, 2019 (Section 35)"
        ],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Information Technology Act, 2000 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_013",
        "category": "online_fraud",
        "complaint": "Fake lottery winner message tricked victim into paying \u20b912,000 processing charges to fraudulent UPI handle.",
        "expected_legal_domain": "Cyber Crime & Information Technology",
        "expected_primary_legislation": "The Information Technology Act, 2000",
        "relevant_sections": [
            "Section 66D"
        ],
        "conditional_sections": [
            "The Consumer Protection Act, 2019 (Section 35)"
        ],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Information Technology Act, 2000 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_014",
        "category": "online_fraud",
        "complaint": "Scammer on OLX sent reverse QR code claiming to pay money and wiped \u20b918,000 from account.",
        "expected_legal_domain": "Cyber Crime & Information Technology",
        "expected_primary_legislation": "The Information Technology Act, 2000",
        "relevant_sections": [
            "Section 66D"
        ],
        "conditional_sections": [
            "The Consumer Protection Act, 2019 (Section 35)"
        ],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Information Technology Act, 2000 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_015",
        "category": "online_fraud",
        "complaint": "Investment crypto scam on Telegram lured victim to deposit \u20b950,000 and blocked withdrawal.",
        "expected_legal_domain": "Cyber Crime & Information Technology",
        "expected_primary_legislation": "The Information Technology Act, 2000",
        "relevant_sections": [
            "Section 66D"
        ],
        "conditional_sections": [
            "The Consumer Protection Act, 2019 (Section 35)"
        ],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Information Technology Act, 2000 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_016",
        "category": "identity_theft",
        "complaint": "Colleague used my Aadhaar card copy and forged signature to obtain an illegal SIM card.",
        "expected_legal_domain": "Cyber Identity Theft & Impersonation",
        "expected_primary_legislation": "The Information Technology Act, 2000",
        "relevant_sections": [
            "Section 66C"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Information Technology Act, 2000 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_017",
        "category": "identity_theft",
        "complaint": "Unknown person created clone Facebook profile using my photos and asked contacts for urgent money.",
        "expected_legal_domain": "Cyber Identity Theft & Impersonation",
        "expected_primary_legislation": "The Information Technology Act, 2000",
        "relevant_sections": [
            "Section 66C"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Information Technology Act, 2000 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_018",
        "category": "identity_theft",
        "complaint": "Hacker obtained my net banking password and conducted unauthorized transactions.",
        "expected_legal_domain": "Cyber Identity Theft & Impersonation",
        "expected_primary_legislation": "The Information Technology Act, 2000",
        "relevant_sections": [
            "Section 66C"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Information Technology Act, 2000 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_019",
        "category": "identity_theft",
        "complaint": "Impersonator created a fake LinkedIn profile using my company credentials to offer bogus consultancies.",
        "expected_legal_domain": "Cyber Identity Theft & Impersonation",
        "expected_primary_legislation": "The Information Technology Act, 2000",
        "relevant_sections": [
            "Section 66C"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Information Technology Act, 2000 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_020",
        "category": "identity_theft",
        "complaint": "Someone used my PAN details without consent to register a GST number in another state.",
        "expected_legal_domain": "Cyber Identity Theft & Impersonation",
        "expected_primary_legislation": "The Information Technology Act, 2000",
        "relevant_sections": [
            "Section 66C"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Information Technology Act, 2000 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_021",
        "category": "defamation",
        "complaint": "Ex-partner created malicious blog posts falsely claiming I am a thief and fraudster to damage my reputation.",
        "expected_legal_domain": "Defamation (Criminal & Civil Tort)",
        "expected_primary_legislation": "The Bharatiya Nyaya Sanhita, 2023",
        "relevant_sections": [
            "Section 356"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal & Civil",
        "expected_reasoning": "Governed primarily by The Bharatiya Nyaya Sanhita, 2023 under Criminal & Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_022",
        "category": "defamation",
        "complaint": "Neighbour distributed printed defamatory pamphlets alleging immoral character across our apartment society.",
        "expected_legal_domain": "Defamation (Criminal & Civil Tort)",
        "expected_primary_legislation": "The Bharatiya Nyaya Sanhita, 2023",
        "relevant_sections": [
            "Section 356"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal & Civil",
        "expected_reasoning": "Governed primarily by The Bharatiya Nyaya Sanhita, 2023 under Criminal & Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_023",
        "category": "defamation",
        "complaint": "Competitor posted fabricated reviews on Google claiming my restaurant serves contaminated food to damage reputation.",
        "expected_legal_domain": "Defamation (Criminal & Civil Tort)",
        "expected_primary_legislation": "The Bharatiya Nyaya Sanhita, 2023",
        "relevant_sections": [
            "Section 356"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal & Civil",
        "expected_reasoning": "Governed primarily by The Bharatiya Nyaya Sanhita, 2023 under Criminal & Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_024",
        "category": "defamation",
        "complaint": "Local news YouTube channel broadcasted unverified defamatory video falsely accusing doctor of malpractice.",
        "expected_legal_domain": "Defamation (Criminal & Civil Tort)",
        "expected_primary_legislation": "The Bharatiya Nyaya Sanhita, 2023",
        "relevant_sections": [
            "Section 356"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal & Civil",
        "expected_reasoning": "Governed primarily by The Bharatiya Nyaya Sanhita, 2023 under Criminal & Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_025",
        "category": "defamation",
        "complaint": "Office rival sent mass email to senior management containing fabricated allegations of corruption to damage my reputation.",
        "expected_legal_domain": "Defamation (Criminal & Civil Tort)",
        "expected_primary_legislation": "The Bharatiya Nyaya Sanhita, 2023",
        "relevant_sections": [
            "Section 356"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal & Civil",
        "expected_reasoning": "Governed primarily by The Bharatiya Nyaya Sanhita, 2023 under Criminal & Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_026",
        "category": "property",
        "complaint": "Adjacent landowner encroached 2 feet into my ancestral agricultural land by erecting a boundary wall.",
        "expected_legal_domain": "Property Law & Civil Possession",
        "expected_primary_legislation": "The Specific Relief Act, 1963",
        "relevant_sections": [
            "Section 5",
            "Section 6"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Specific Relief Act, 1963 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_027",
        "category": "property",
        "complaint": "Seller signed registered sale agreement for house, took advance \u20b95,00,000, but now refuses to execute sale deed.",
        "expected_legal_domain": "Property Law & Civil Possession",
        "expected_primary_legislation": "The Transfer of Property Act, 1882",
        "relevant_sections": [
            "Section 54"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Transfer of Property Act, 1882 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_028",
        "category": "property",
        "complaint": "Distant relative attempting to forcibly dispossess me from my self-acquired residential property.",
        "expected_legal_domain": "Property Law & Civil Possession",
        "expected_primary_legislation": "The Specific Relief Act, 1963",
        "relevant_sections": [
            "Section 38"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Specific Relief Act, 1963 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_029",
        "category": "property",
        "complaint": "Commercial sub-tenant refusing to vacate premises after expiry of 5-year registered lease deed.",
        "expected_legal_domain": "Property Law & Civil Possession",
        "expected_primary_legislation": "The Transfer of Property Act, 1882",
        "relevant_sections": [
            "Section 105"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Transfer of Property Act, 1882 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_030",
        "category": "property",
        "complaint": "Donor challenging registered gift deed made 4 years ago after change of mind.",
        "expected_legal_domain": "Property Law & Civil Possession",
        "expected_primary_legislation": "The Transfer of Property Act, 1882",
        "relevant_sections": [
            "Section 122"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Transfer of Property Act, 1882 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_031",
        "category": "employment",
        "complaint": "Software company withheld my 3 months salary of \u20b91,80,000 after I tendered resignation with notice.",
        "expected_legal_domain": "Labour & Employment Law",
        "expected_primary_legislation": "The Payment of Wages Act, 1936",
        "relevant_sections": [
            "Section 15"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Labour / Civil",
        "expected_reasoning": "Governed primarily by The Payment of Wages Act, 1936 under Labour / Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_032",
        "category": "employment",
        "complaint": "Factory management terminated senior machine operator without enquiry or retrenchment compensation.",
        "expected_legal_domain": "Labour & Employment Law",
        "expected_primary_legislation": "The Industrial Disputes Act, 1947",
        "relevant_sections": [
            "Section 2A"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Labour / Civil",
        "expected_reasoning": "Governed primarily by The Industrial Disputes Act, 1947 under Labour / Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_033",
        "category": "employment",
        "complaint": "Hotel refused to pay statutory gratuity to waiter who completed 7 continuous years of service.",
        "expected_legal_domain": "Labour & Employment Law",
        "expected_primary_legislation": "The Payment of Gratuity Act, 1972",
        "relevant_sections": [
            "Section 7"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Labour / Civil",
        "expected_reasoning": "Governed primarily by The Payment of Gratuity Act, 1972 under Labour / Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_034",
        "category": "employment",
        "complaint": "Retail store owner made arbitrary salary deductions of \u20b910,000 claiming inventory shortfall.",
        "expected_legal_domain": "Labour & Employment Law",
        "expected_primary_legislation": "The Payment of Wages Act, 1936",
        "relevant_sections": [
            "Section 15"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Labour / Civil",
        "expected_reasoning": "Governed primarily by The Payment of Wages Act, 1936 under Labour / Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_035",
        "category": "employment",
        "complaint": "Private school terminated female teacher after she applied for 26 weeks statutory maternity leave.",
        "expected_legal_domain": "Labour & Employment Law",
        "expected_primary_legislation": "The Maternity Benefit Act, 1961",
        "relevant_sections": [
            "Section 5",
            "Section 12"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Labour / Civil",
        "expected_reasoning": "Governed primarily by The Maternity Benefit Act, 1961 under Labour / Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_036",
        "category": "workplace_harassment",
        "complaint": "Department head made unwelcome sexual advances and threatened poor appraisal if I did not comply.",
        "expected_legal_domain": "Workplace Sexual Harassment & Gender Protection",
        "expected_primary_legislation": "The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act)",
        "relevant_sections": [
            "Section 4",
            "Section 9"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Regulatory & Criminal",
        "expected_reasoning": "Governed primarily by The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act) under Regulatory & Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_037",
        "category": "workplace_harassment",
        "complaint": "Colleague at tech company sent sexually explicit jokes and inappropriate messages on office Slack.",
        "expected_legal_domain": "Workplace Sexual Harassment & Gender Protection",
        "expected_primary_legislation": "The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act)",
        "relevant_sections": [
            "Section 4",
            "Section 9"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Regulatory & Criminal",
        "expected_reasoning": "Governed primarily by The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act) under Regulatory & Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_038",
        "category": "workplace_harassment",
        "complaint": "Company HR refused to accept sexual harassment complaint saying firm has no Internal Committee.",
        "expected_legal_domain": "Workplace Sexual Harassment & Gender Protection",
        "expected_primary_legislation": "The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act)",
        "relevant_sections": [
            "Section 4",
            "Section 9"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Regulatory & Criminal",
        "expected_reasoning": "Governed primarily by The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act) under Regulatory & Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_039",
        "category": "workplace_harassment",
        "complaint": "Senior executive subjected junior female employee to unwelcome physical touching during official offsite dinner.",
        "expected_legal_domain": "Workplace Sexual Harassment & Gender Protection",
        "expected_primary_legislation": "The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act)",
        "relevant_sections": [
            "Section 4",
            "Section 9"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Regulatory & Criminal",
        "expected_reasoning": "Governed primarily by The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act) under Regulatory & Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_040",
        "category": "workplace_harassment",
        "complaint": "Male colleague stalking female employee in office parking lot and sending inappropriate messages.",
        "expected_legal_domain": "Workplace Sexual Harassment & Gender Protection",
        "expected_primary_legislation": "The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act)",
        "relevant_sections": [
            "Section 4",
            "Section 9"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Regulatory & Criminal",
        "expected_reasoning": "Governed primarily by The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act) under Regulatory & Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_041",
        "category": "road_accident",
        "complaint": "Drunk truck driver jumped red light and rammed into our family car causing severe permanent disability.",
        "expected_legal_domain": "Motor Accident Claims & Criminal Negligence",
        "expected_primary_legislation": "The Motor Vehicles Act, 1988",
        "relevant_sections": [
            "Section 166"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil & Criminal",
        "expected_reasoning": "Governed primarily by The Motor Vehicles Act, 1988 under Civil & Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_042",
        "category": "road_accident",
        "complaint": "Speeding private bus hit pedestrian crossing road at zebra crossing resulting in fatal head injuries.",
        "expected_legal_domain": "Motor Accident Claims & Criminal Negligence",
        "expected_primary_legislation": "The Motor Vehicles Act, 1988",
        "relevant_sections": [
            "Section 166"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil & Criminal",
        "expected_reasoning": "Governed primarily by The Motor Vehicles Act, 1988 under Civil & Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_043",
        "category": "road_accident",
        "complaint": "Two-wheeler rider hit by negligent SUV driver reversing recklessly in residential street.",
        "expected_legal_domain": "Motor Accident Claims & Criminal Negligence",
        "expected_primary_legislation": "The Motor Vehicles Act, 1988",
        "relevant_sections": [
            "Section 166"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil & Criminal",
        "expected_reasoning": "Governed primarily by The Motor Vehicles Act, 1988 under Civil & Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_044",
        "category": "road_accident",
        "complaint": "Hit-and-run taxi knocked down cyclist at night leaving victim with fractured leg.",
        "expected_legal_domain": "Motor Accident Claims & Criminal Negligence",
        "expected_primary_legislation": "The Motor Vehicles Act, 1988",
        "relevant_sections": [
            "Section 166"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil & Criminal",
        "expected_reasoning": "Governed primarily by The Motor Vehicles Act, 1988 under Civil & Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_045",
        "category": "road_accident",
        "complaint": "Delivery van driver driving rashly collided with autorickshaw injuring three passengers.",
        "expected_legal_domain": "Motor Accident Claims & Criminal Negligence",
        "expected_primary_legislation": "The Motor Vehicles Act, 1988",
        "relevant_sections": [
            "Section 166"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil & Criminal",
        "expected_reasoning": "Governed primarily by The Motor Vehicles Act, 1988 under Civil & Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_046",
        "category": "domestic_violence",
        "complaint": "Husband and in-laws subjected wife to physical abuse and threw her out of matrimonial home.",
        "expected_legal_domain": "Family Law & Domestic Violence Protection",
        "expected_primary_legislation": "Protection of Women from Domestic Violence Act, 2005",
        "relevant_sections": [
            "Section 12",
            "Section 18"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil & Quasi-Criminal",
        "expected_reasoning": "Governed primarily by Protection of Women from Domestic Violence Act, 2005 under Civil & Quasi-Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_047",
        "category": "domestic_violence",
        "complaint": "Woman locked out of shared household by in-laws after husband relocated abroad.",
        "expected_legal_domain": "Family Law & Domestic Violence Protection",
        "expected_primary_legislation": "Protection of Women from Domestic Violence Act, 2005",
        "relevant_sections": [
            "Section 12",
            "Section 19"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil & Quasi-Criminal",
        "expected_reasoning": "Governed primarily by Protection of Women from Domestic Violence Act, 2005 under Civil & Quasi-Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_048",
        "category": "domestic_violence",
        "complaint": "Wife denied basic food, medical expenses, and pocket money by alcoholic husband.",
        "expected_legal_domain": "Family Law & Domestic Violence Protection",
        "expected_primary_legislation": "Protection of Women from Domestic Violence Act, 2005",
        "relevant_sections": [
            "Section 12",
            "Section 20"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil & Quasi-Criminal",
        "expected_reasoning": "Governed primarily by Protection of Women from Domestic Violence Act, 2005 under Civil & Quasi-Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_049",
        "category": "domestic_violence",
        "complaint": "Elderly mother facing continuous verbal abuse, threats, and eviction by married son in shared residence.",
        "expected_legal_domain": "Family Law & Domestic Violence Protection",
        "expected_primary_legislation": "Protection of Women from Domestic Violence Act, 2005",
        "relevant_sections": [
            "Section 12",
            "Section 23"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil & Quasi-Criminal",
        "expected_reasoning": "Governed primarily by Protection of Women from Domestic Violence Act, 2005 under Civil & Quasi-Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_050",
        "category": "domestic_violence",
        "complaint": "Husband threatening wife with physical harm and attempting to forcefully alienate Stridhan jewelry.",
        "expected_legal_domain": "Family Law & Domestic Violence Protection",
        "expected_primary_legislation": "Protection of Women from Domestic Violence Act, 2005",
        "relevant_sections": [
            "Section 12",
            "Section 18"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil & Quasi-Criminal",
        "expected_reasoning": "Governed primarily by Protection of Women from Domestic Violence Act, 2005 under Civil & Quasi-Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_051",
        "category": "maintenance",
        "complaint": "Husband deserted unemployed wife and 4-year-old child without providing any monthly financial maintenance.",
        "expected_legal_domain": "Family Law & Maintenance",
        "expected_primary_legislation": "Section 125 CrPC / Section 144 BNSS",
        "relevant_sections": [
            "Section 125 CrPC / Section 144 BNSS"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Quasi-Criminal / Civil",
        "expected_reasoning": "Governed primarily by Section 125 CrPC / Section 144 BNSS under Quasi-Criminal / Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_052",
        "category": "maintenance",
        "complaint": "Elderly parents abandoned by earning son seeking statutory monthly maintenance under Senior Citizens Act.",
        "expected_legal_domain": "Family Law & Maintenance",
        "expected_primary_legislation": "Section 125 CrPC / Section 144 BNSS",
        "relevant_sections": [
            "Section 125 CrPC / Section 144 BNSS"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Quasi-Criminal / Civil",
        "expected_reasoning": "Governed primarily by Section 125 CrPC / Section 144 BNSS under Quasi-Criminal / Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_053",
        "category": "maintenance",
        "complaint": "Wife seeking interim monetary relief and school fees for children during pending divorce proceedings.",
        "expected_legal_domain": "Family Law & Maintenance",
        "expected_primary_legislation": "Protection of Women from Domestic Violence Act, 2005",
        "relevant_sections": [
            "Section 20"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Quasi-Criminal / Civil",
        "expected_reasoning": "Governed primarily by Protection of Women from Domestic Violence Act, 2005 under Quasi-Criminal / Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_054",
        "category": "maintenance",
        "complaint": "Wife with no independent source of income seeking enhancement of maintenance awarded 3 years ago.",
        "expected_legal_domain": "Family Law & Maintenance",
        "expected_primary_legislation": "Section 125 CrPC / Section 144 BNSS",
        "relevant_sections": [
            "Section 125 CrPC / Section 144 BNSS"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Quasi-Criminal / Civil",
        "expected_reasoning": "Governed primarily by Section 125 CrPC / Section 144 BNSS under Quasi-Criminal / Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_055",
        "category": "maintenance",
        "complaint": "Husband concealing high corporate salary in maintenance proceedings to evade realistic support for disabled child.",
        "expected_legal_domain": "Family Law & Maintenance",
        "expected_primary_legislation": "Section 125 CrPC / Section 144 BNSS",
        "relevant_sections": [
            "Section 125 CrPC / Section 144 BNSS"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Quasi-Criminal / Civil",
        "expected_reasoning": "Governed primarily by Section 125 CrPC / Section 144 BNSS under Quasi-Criminal / Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_056",
        "category": "consumer",
        "complaint": "Purchased defective smart TV from authorized retailer that stopped displaying picture in 10 days.",
        "expected_legal_domain": "Consumer Protection & Product Liability",
        "expected_primary_legislation": "The Consumer Protection Act, 2019",
        "relevant_sections": [
            "Section 2(7)",
            "Section 35"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Indian Penal Code, 1860"
        ],
        "expected_legal_classification": "Consumer",
        "expected_reasoning": "Governed primarily by The Consumer Protection Act, 2019 under Consumer legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_057",
        "category": "consumer",
        "complaint": "Airline cancelled domestic flight unilaterally without offering alternative flight or fare refund.",
        "expected_legal_domain": "Consumer Protection & Product Liability",
        "expected_primary_legislation": "The Consumer Protection Act, 2019",
        "relevant_sections": [
            "Section 2(7)",
            "Section 35"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Indian Penal Code, 1860"
        ],
        "expected_legal_classification": "Consumer",
        "expected_reasoning": "Governed primarily by The Consumer Protection Act, 2019 under Consumer legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_058",
        "category": "consumer",
        "complaint": "E-commerce platform delivered counterfeit shoes instead of genuine brand and refused return.",
        "expected_legal_domain": "Consumer Protection & Product Liability",
        "expected_primary_legislation": "The Consumer Protection Act, 2019",
        "relevant_sections": [
            "Section 2(7)",
            "Section 35"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Indian Penal Code, 1860"
        ],
        "expected_legal_classification": "Consumer",
        "expected_reasoning": "Governed primarily by The Consumer Protection Act, 2019 under Consumer legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_059",
        "category": "consumer",
        "complaint": "Automobile service centre damaged car engine during routine periodic service and demanded \u20b940,000.",
        "expected_legal_domain": "Consumer Protection & Product Liability",
        "expected_primary_legislation": "The Consumer Protection Act, 2019",
        "relevant_sections": [
            "Section 2(7)",
            "Section 35"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Indian Penal Code, 1860"
        ],
        "expected_legal_classification": "Consumer",
        "expected_reasoning": "Governed primarily by The Consumer Protection Act, 2019 under Consumer legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_060",
        "category": "consumer",
        "complaint": "Health insurance company rejected genuine hospitalization claim falsely citing non-disclosure.",
        "expected_legal_domain": "Consumer Protection & Product Liability",
        "expected_primary_legislation": "The Consumer Protection Act, 2019",
        "relevant_sections": [
            "Section 2(7)",
            "Section 35"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Indian Penal Code, 1860"
        ],
        "expected_legal_classification": "Consumer",
        "expected_reasoning": "Governed primarily by The Consumer Protection Act, 2019 under Consumer legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_061",
        "category": "ip_disputes",
        "complaint": "Rival shop opened with identical trademark logo and phonetically identical brand name to deceive customers.",
        "expected_legal_domain": "Intellectual Property & Trademark Law",
        "expected_primary_legislation": "The Trade Marks Act, 1999",
        "relevant_sections": [
            "Section 29"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil & Criminal",
        "expected_reasoning": "Governed primarily by The Trade Marks Act, 1999 under Civil & Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_062",
        "category": "ip_disputes",
        "complaint": "Online coaching channel downloaded and re-uploaded my copyrighted educational videos without permission.",
        "expected_legal_domain": "Intellectual Property & Copyright Law",
        "expected_primary_legislation": "The Copyright Act, 1957",
        "relevant_sections": [
            "Section 51"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil & Criminal",
        "expected_reasoning": "Governed primarily by The Copyright Act, 1957 under Civil & Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_063",
        "category": "ip_disputes",
        "complaint": "Manufacturer seeking temporary and permanent injunction against counterfeit goods bearing registered trademark.",
        "expected_legal_domain": "Intellectual Property & Trademark Law",
        "expected_primary_legislation": "The Trade Marks Act, 1999",
        "relevant_sections": [
            "Section 134",
            "Section 135"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Trade Marks Act, 1999 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_064",
        "category": "ip_disputes",
        "complaint": "Commercial software pirated and distributed on torrent sites causing severe economic injury to developer.",
        "expected_legal_domain": "Intellectual Property & Copyright Law",
        "expected_primary_legislation": "The Copyright Act, 1957",
        "relevant_sections": [
            "Section 63"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Copyright Act, 1957 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_065",
        "category": "ip_disputes",
        "complaint": "Competitor infringing patented medical diagnostic kit manufactured under granted Indian patent.",
        "expected_legal_domain": "Intellectual Property & Patent Law",
        "expected_primary_legislation": "The Patents Act, 1970",
        "relevant_sections": [
            "Section 108"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Patents Act, 1970 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_066",
        "category": "cbt",
        "complaint": "Accountant entrusted with company cash chest misappropriated \u20b92,00,000 for personal gambling.",
        "expected_legal_domain": "Criminal Law & Offences Against Property",
        "expected_primary_legislation": "The Bharatiya Nyaya Sanhita, 2023",
        "relevant_sections": [
            "Section 316"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Bharatiya Nyaya Sanhita, 2023 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_067",
        "category": "cbt",
        "complaint": "Gave gold jewelry to goldsmith for repair, who pledged it with pawn broker and absconded.",
        "expected_legal_domain": "Criminal Law & Offences Against Property",
        "expected_primary_legislation": "The Bharatiya Nyaya Sanhita, 2023",
        "relevant_sections": [
            "Section 316"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Bharatiya Nyaya Sanhita, 2023 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_068",
        "category": "cbt",
        "complaint": "Warehouse manager dishonestly sold 50 bags of entrusted basmati rice and pocketed the proceeds.",
        "expected_legal_domain": "Criminal Law & Offences Against Property",
        "expected_primary_legislation": "The Bharatiya Nyaya Sanhita, 2023",
        "relevant_sections": [
            "Section 316"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Bharatiya Nyaya Sanhita, 2023 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_069",
        "category": "cbt",
        "complaint": "Vehicle custodian entrusted with fleet car for airport transport pledged vehicle for illegal loan.",
        "expected_legal_domain": "Criminal Law & Offences Against Property",
        "expected_primary_legislation": "The Bharatiya Nyaya Sanhita, 2023",
        "relevant_sections": [
            "Section 316"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Bharatiya Nyaya Sanhita, 2023 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_070",
        "category": "cbt",
        "complaint": "Partner in firm withdrew partnership funds from bank account and converted them to personal assets.",
        "expected_legal_domain": "Criminal Law & Offences Against Property",
        "expected_primary_legislation": "The Bharatiya Nyaya Sanhita, 2023",
        "relevant_sections": [
            "Section 316"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Bharatiya Nyaya Sanhita, 2023 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_071",
        "category": "cheating",
        "complaint": "Person claiming to be government official took \u20b950,000 promising ration shop license and vanished.",
        "expected_legal_domain": "Criminal Fraud, Cheating & Cyber Crime",
        "expected_primary_legislation": "The Bharatiya Nyaya Sanhita, 2023",
        "relevant_sections": [
            "Section 318(4)"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Bharatiya Nyaya Sanhita, 2023 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_072",
        "category": "cheating",
        "complaint": "Builder showed fake approval plan, collected \u20b910,00,000 booking advance, and had no land title.",
        "expected_legal_domain": "Criminal Fraud, Cheating & Cyber Crime",
        "expected_primary_legislation": "The Bharatiya Nyaya Sanhita, 2023",
        "relevant_sections": [
            "Section 318(4)"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Bharatiya Nyaya Sanhita, 2023 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_073",
        "category": "cheating",
        "complaint": "Fake travel agent collected passport and \u20b940,000 for foreign visa and gave forged counterfeit sticker.",
        "expected_legal_domain": "Criminal Fraud, Cheating & Cyber Crime",
        "expected_primary_legislation": "The Bharatiya Nyaya Sanhita, 2023",
        "relevant_sections": [
            "Section 318(4)"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Bharatiya Nyaya Sanhita, 2023 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_074",
        "category": "cheating",
        "complaint": "Conman sold brass ornaments inducing victim to believe it was genuine 22-karat hallmarked gold.",
        "expected_legal_domain": "Criminal Fraud, Cheating & Cyber Crime",
        "expected_primary_legislation": "The Bharatiya Nyaya Sanhita, 2023",
        "relevant_sections": [
            "Section 318(4)"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Bharatiya Nyaya Sanhita, 2023 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_075",
        "category": "cheating",
        "complaint": "Phony educational consultancy collected \u20b975,000 promising direct MBBS admission in government college.",
        "expected_legal_domain": "Criminal Fraud, Cheating & Cyber Crime",
        "expected_primary_legislation": "The Bharatiya Nyaya Sanhita, 2023",
        "relevant_sections": [
            "Section 318(4)"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Bharatiya Nyaya Sanhita, 2023 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_076",
        "category": "finder_goods",
        "complaint": "I found lost spectacles advertised in newspaper with \u20b91,000 reward, but owner refused to pay reward upon return.",
        "expected_legal_domain": "Law of Contracts & Bailment (Finder of Goods)",
        "expected_primary_legislation": "The Indian Contract Act, 1872",
        "relevant_sections": [
            "Section 168",
            "Section 8"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Indian Contract Act, 1872 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_077",
        "category": "finder_goods",
        "complaint": "Owner posted poster promising \u20b95,000 reward for finding lost wallet. I returned wallet with cards, owner gave nothing.",
        "expected_legal_domain": "Law of Contracts & Bailment (Finder of Goods)",
        "expected_primary_legislation": "The Indian Contract Act, 1872",
        "relevant_sections": [
            "Section 168",
            "Section 8"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Indian Contract Act, 1872 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_078",
        "category": "finder_goods",
        "complaint": "Finder returned lost golden ring after seeing public social media reward post of \u20b910,000; owner refused payment.",
        "expected_legal_domain": "Law of Contracts & Bailment (Finder of Goods)",
        "expected_primary_legislation": "The Indian Contract Act, 1872",
        "relevant_sections": [
            "Section 168",
            "Section 8"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Indian Contract Act, 1872 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_079",
        "category": "finder_goods",
        "complaint": "Found lost pedigree dog advertised with \u20b93,000 reward. Owner retrieved dog but reneged on promised reward.",
        "expected_legal_domain": "Law of Contracts & Bailment (Finder of Goods)",
        "expected_primary_legislation": "The Indian Contract Act, 1872",
        "relevant_sections": [
            "Section 168",
            "Section 8"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Indian Contract Act, 1872 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_080",
        "category": "finder_goods",
        "complaint": "Citizen found lost official passport with reward announcement of \u20b92,500; traveler refused to honor reward.",
        "expected_legal_domain": "Law of Contracts & Bailment (Finder of Goods)",
        "expected_primary_legislation": "The Indian Contract Act, 1872",
        "relevant_sections": [
            "Section 168",
            "Section 8"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Indian Contract Act, 1872 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_081",
        "category": "personal_loan",
        "complaint": "Friend borrowed \u20b930,000 via Google Pay promising to return in 10 days, but has not returned for 8 months.",
        "expected_legal_domain": "Civil Debt Recovery & Law of Contracts",
        "expected_primary_legislation": "The Indian Contract Act, 1872",
        "relevant_sections": [
            "Section 73"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Indian Contract Act, 1872 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_082",
        "category": "personal_loan",
        "complaint": "Lent \u20b91,00,000 to brother-in-law on written promissory note for medical treatment, he is now refusing to pay back.",
        "expected_legal_domain": "Civil Debt Recovery & Law of Contracts",
        "expected_primary_legislation": "The Indian Contract Act, 1872",
        "relevant_sections": [
            "Section 73"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Indian Contract Act, 1872 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_083",
        "category": "personal_loan",
        "complaint": "Colleague borrowed \u20b925,000 cash for house deposit promising repayment on salary day, but avoided payment.",
        "expected_legal_domain": "Civil Debt Recovery & Law of Contracts",
        "expected_primary_legislation": "The Indian Contract Act, 1872",
        "relevant_sections": [
            "Section 73"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Indian Contract Act, 1872 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_084",
        "category": "personal_loan",
        "complaint": "Neighbour borrowed \u20b960,000 promising interest and principal within 3 months, now denies borrowing.",
        "expected_legal_domain": "Civil Debt Recovery & Law of Contracts",
        "expected_primary_legislation": "The Indian Contract Act, 1872",
        "relevant_sections": [
            "Section 73"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Indian Contract Act, 1872 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_085",
        "category": "personal_loan",
        "complaint": "Lent \u20b940,000 to childhood friend via bank transfer. Friend says he will not repay and dares me to go to court.",
        "expected_legal_domain": "Civil Debt Recovery & Law of Contracts",
        "expected_primary_legislation": "The Indian Contract Act, 1872",
        "relevant_sections": [
            "Section 73"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Indian Contract Act, 1872 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_086",
        "category": "cyberstalking",
        "complaint": "Unknown stalker constantly monitoring my Instagram stories and sending vulgar photos from burner accounts.",
        "expected_legal_domain": "Cyber Harassment & IT Law",
        "expected_primary_legislation": "The Information Technology Act, 2000",
        "relevant_sections": [
            "Section 66E",
            "Section 67"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Information Technology Act, 2000 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_087",
        "category": "cyberstalking",
        "complaint": "Ex-boyfriend threatening to circulate private intimate photos online unless I agree to meet him.",
        "expected_legal_domain": "Cyber Harassment & IT Law",
        "expected_primary_legislation": "The Information Technology Act, 2000",
        "relevant_sections": [
            "Section 66E",
            "Section 67A"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Information Technology Act, 2000 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_088",
        "category": "cyberstalking",
        "complaint": "Gym trainer secretly captured video inside changing room and shared on private group.",
        "expected_legal_domain": "Cyber Harassment & IT Law",
        "expected_primary_legislation": "The Information Technology Act, 2000",
        "relevant_sections": [
            "Section 66E"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Information Technology Act, 2000 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_089",
        "category": "cyberstalking",
        "complaint": "Troll sending obscene emails and morphing female student's photos on social media.",
        "expected_legal_domain": "Cyber Harassment & IT Law",
        "expected_primary_legislation": "The Information Technology Act, 2000",
        "relevant_sections": [
            "Section 67"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Information Technology Act, 2000 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_090",
        "category": "cyberstalking",
        "complaint": "Person installed spyware on victim's phone to track real-time GPS location and WhatsApp chats.",
        "expected_legal_domain": "Cyber Harassment & IT Law",
        "expected_primary_legislation": "The Information Technology Act, 2000",
        "relevant_sections": [
            "Section 66E"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Criminal",
        "expected_reasoning": "Governed primarily by The Information Technology Act, 2000 under Criminal legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_091",
        "category": "rent_deposit",
        "complaint": "Landlord in Chennai refusing to return \u20b950,000 advance after tenant vacated flat with key handover.",
        "expected_legal_domain": "Tenancy & Immovable Property Law",
        "expected_primary_legislation": "State Tenancy / TNRRLTA",
        "relevant_sections": [
            "Section 10(2)"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by State Tenancy / TNRRLTA under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_092",
        "category": "rent_deposit",
        "complaint": "Owner deducted \u20b930,000 for regular painting wear-and-tear and refuses to furnish itemized bills.",
        "expected_legal_domain": "Tenancy & Immovable Property Law",
        "expected_primary_legislation": "State Tenancy / TNRRLTA",
        "relevant_sections": [
            "Section 10(2)"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by State Tenancy / TNRRLTA under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_093",
        "category": "rent_deposit",
        "complaint": "Landlord disconnected water and power supply to force immediate eviction without statutory notice.",
        "expected_legal_domain": "Tenancy & Immovable Property Law",
        "expected_primary_legislation": "The Transfer of Property Act, 1882",
        "relevant_sections": [
            "Section 106"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by The Transfer of Property Act, 1882 under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_094",
        "category": "rent_deposit",
        "complaint": "Tenant vacated 3 months ago but landlord continues to delay refund saying new tenant has not arrived.",
        "expected_legal_domain": "Tenancy & Immovable Property Law",
        "expected_primary_legislation": "State Tenancy / TNRRLTA",
        "relevant_sections": [
            "Section 10(2)"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by State Tenancy / TNRRLTA under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_095",
        "category": "rent_deposit",
        "complaint": "Landlord demanding 25% rent increase mid-lease and threatening eviction if not agreed.",
        "expected_legal_domain": "Tenancy & Immovable Property Law",
        "expected_primary_legislation": "State Tenancy / TNRRLTA",
        "relevant_sections": [
            "Section 21"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Civil",
        "expected_reasoning": "Governed primarily by State Tenancy / TNRRLTA under Civil legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_096",
        "category": "education",
        "complaint": "College refusing to issue hall ticket for final exam alleging university portal technical fee glitch.",
        "expected_legal_domain": "Higher Education & Student Grievances",
        "expected_primary_legislation": "UGC (Redressal of Grievances of Students) Regulations, 2023",
        "relevant_sections": [
            "Regulation 5",
            "Regulation 6"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Regulatory & Administrative",
        "expected_reasoning": "Governed primarily by UGC (Redressal of Grievances of Students) Regulations, 2023 under Regulatory & Administrative legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_097",
        "category": "education",
        "complaint": "Private college withholding original 10th and 12th marksheets after student withdrew admission.",
        "expected_legal_domain": "Higher Education & Student Grievances",
        "expected_primary_legislation": "UGC (Redressal of Grievances of Students) Regulations, 2023",
        "relevant_sections": [
            "Regulation 5"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Regulatory & Administrative",
        "expected_reasoning": "Governed primarily by UGC (Redressal of Grievances of Students) Regulations, 2023 under Regulatory & Administrative legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_098",
        "category": "education",
        "complaint": "University refusing refund of tuition fee after student surrendered seat before admission deadline.",
        "expected_legal_domain": "Higher Education & Student Grievances",
        "expected_primary_legislation": "UGC (Redressal of Grievances of Students) Regulations, 2023",
        "relevant_sections": [
            "Regulation 5"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Regulatory & Administrative",
        "expected_reasoning": "Governed primarily by UGC (Redressal of Grievances of Students) Regulations, 2023 under Regulatory & Administrative legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_099",
        "category": "education",
        "complaint": "College refusing to issue provisional degree certificate demanding unauthorized alumni fund donation.",
        "expected_legal_domain": "Higher Education & Student Grievances",
        "expected_primary_legislation": "UGC (Redressal of Grievances of Students) Regulations, 2023",
        "relevant_sections": [
            "Regulation 5"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Regulatory & Administrative",
        "expected_reasoning": "Governed primarily by UGC (Redressal of Grievances of Students) Regulations, 2023 under Regulatory & Administrative legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    },
    {
        "id": "scenario_100",
        "category": "education",
        "complaint": "Autonomous engineering college debarred student from campus placement without written enquiry.",
        "expected_legal_domain": "Higher Education & Student Grievances",
        "expected_primary_legislation": "UGC (Redressal of Grievances of Students) Regulations, 2023",
        "relevant_sections": [
            "Regulation 5"
        ],
        "conditional_sections": [],
        "irrelevant_legislation": [
            "The Consumer Protection Act, 2019"
        ],
        "expected_legal_classification": "Regulatory & Administrative",
        "expected_reasoning": "Governed primarily by UGC (Redressal of Grievances of Students) Regulations, 2023 under Regulatory & Administrative legal jurisdiction.",
        "official_reference_sources": [
            "India Code Legislative Repository",
            "Supreme Court of India Precedents"
        ]
    }
]
