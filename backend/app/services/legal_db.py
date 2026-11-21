"""
Authoritative Indian Statutory & Judicial Precedents Knowledge Base.
Contains verified statutory provisions, enactment/commencement dates,
repeal chains, and landmark Supreme Court & High Court precedents.
"""

from datetime import datetime
from typing import Optional, Dict, Any, List

# ── Statutory Provisions Registry ─────────────────────────────────────────────

STATUTES_REGISTRY: Dict[str, Dict[str, Any]] = {
    "consumer protection act, 2019": {
        "official_name": "The Consumer Protection Act, 2019",
        "act_number": "Act No. 35 of 2019",
        "enactment_date": "2019-08-09",
        "commencement_date": "2020-07-20",
        "status": "in_force",
        "repealed_laws": ["The Consumer Protection Act, 1986"],
        "official_source": "https://www.indiacode.nic.in/handle/123456789/15256",
        "jurisdiction": "India (Central)",
        "max_section": 107,
        "sections": {
            "2(7)": {
                "title": "Definition of Consumer",
                "text": "Any person who buys any goods for a consideration or hires or avails of any service for a consideration, but does not include a person who obtains such goods for resale or for any commercial purpose.",
                "claim_type": "statutory",
                "topic": "consumer definition"
            },
            "2(11)": {
                "title": "Definition of Deficiency",
                "text": "Any fault, imperfection, shortcoming or inadequacy in the quality, nature and manner of performance which is required to be maintained by or under any law for the time being in force or has been undertaken to be performed by a person in pursuance of a contract or otherwise in relation to any service.",
                "claim_type": "statutory",
                "topic": "deficiency in service"
            },
            "2(42)": {
                "title": "Definition of Service",
                "text": "Service of any description which is made available to potential users and includes banking, financing, insurance, transport, processing, supply of electrical or other energy, telecom, boarding or lodging or both, housing construction, entertainment, amusement or the purveying of news or other information, but does not include the rendering of any service free of charge or under a contract of personal service or sovereign statutory functions.",
                "claim_type": "statutory",
                "topic": "service definition"
            },
            "34": {
                "title": "Jurisdiction of District Commission",
                "text": "District Commission shall have jurisdiction to entertain complaints where the value of the goods or services paid as consideration does not exceed fifty lakh rupees (revised by notification under 2019 Act).",
                "claim_type": "statutory",
                "topic": "pecuniary jurisdiction district"
            },
            "35": {
                "title": "Manner in which complaint shall be made",
                "text": "A complaint, in relation to any goods sold or delivered or agreed to be sold or delivered or any service provided or agreed to be provided, may be filed with a District Commission by the consumer, or any recognized consumer association, or Central Authority.",
                "claim_type": "statutory",
                "topic": "filing consumer complaint"
            },
            "38": {
                "title": "Procedure on admission of complaint",
                "text": "The District Commission shall refer a copy of the admitted complaint to the opposite party directing him to give his version of the case within a period of thirty days or such extended period not exceeding fifteen days as may be granted by the District Commission.",
                "claim_type": "statutory",
                "topic": "notice procedure opposite party deadline"
            },
            "69": {
                "title": "Limitation period",
                "text": "The District Commission, the State Commission or the National Commission shall not admit a complaint unless it is filed within two years from the date on which the cause of action has arisen.",
                "claim_type": "statutory",
                "topic": "limitation period 2 years"
            }
        }
    },
    "consumer protection act, 1986": {
        "official_name": "The Consumer Protection Act, 1986",
        "act_number": "Act No. 68 of 1986",
        "enactment_date": "1986-12-24",
        "commencement_date": "1987-04-15",
        "status": "repealed",
        "repealed_by": "The Consumer Protection Act, 2019 (w.e.f. 20 July 2020)",
        "official_source": "https://www.indiacode.nic.in/",
        "jurisdiction": "India (Central)",
        "max_section": 31,
        "sections": {}
    },
    "negotiable instruments act, 1881": {
        "official_name": "The Negotiable Instruments Act, 1881",
        "act_number": "Act No. 26 of 1881",
        "enactment_date": "1881-12-09",
        "commencement_date": "1882-03-01",
        "status": "in_force",
        "official_source": "https://www.indiacode.nic.in/handle/123456789/2187",
        "jurisdiction": "India (Central)",
        "max_section": 148,
        "sections": {
            "138": {
                "title": "Dishonour of cheque for insufficiency, etc., of funds in the account",
                "text": "Where any cheque drawn by a person on an account maintained by him with a banker for payment of any amount of money to another person from out of that account for the discharge, in whole or in part, of any debt or other liability, is returned by the bank unpaid, such person shall be deemed to have committed an offence. Statutory demand notice must be issued within 30 days of receipt of bank memo. Drawer has 15 days to pay from receipt of notice.",
                "claim_type": "statutory",
                "topic": "cheque bounce dishonour"
            },
            "141": {
                "title": "Offences by companies",
                "text": "If the person committing an offence under section 138 is a company, every person who, at the time the offence was committed, was in charge of, and was responsible to the company for the conduct of the business of the company, as well as the company, shall be deemed to be guilty of the offence.",
                "claim_type": "statutory",
                "topic": "director liability cheque bounce"
            },
            "142": {
                "title": "Cognizance of offences",
                "text": "No court shall take cognizance of any offence punishable under section 138 except upon a complaint, in writing, made by the payee or, as the case may be, the holder in due course of the cheque within one month of the date on which the cause-of-action arises under clause (c) of the proviso to section 138.",
                "claim_type": "statutory",
                "topic": "cognizance limitation one month"
            }
        }
    },
    "information technology act, 2000": {
        "official_name": "The Information Technology Act, 2000",
        "act_number": "Act No. 21 of 2000",
        "enactment_date": "2000-06-09",
        "commencement_date": "2000-10-17",
        "status": "in_force",
        "official_source": "https://www.indiacode.nic.in/handle/123456789/1999",
        "jurisdiction": "India (Central)",
        "max_section": 94,
        "sections": {
            "43": {
                "title": "Penalty and compensation for damage to computer, computer system, etc.",
                "text": "If any person without permission of the owner damages, copies, extracts data, introduces virus, or disrupts any computer system, he shall be liable to pay damages by way of compensation to the person so affected.",
                "claim_type": "statutory",
                "topic": "unauthorized access civil compensation"
            },
            "66": {
                "title": "Computer related offences",
                "text": "If any person, dishonestly or fraudulently, does any act referred to in section 43, he shall be punishable with imprisonment for a term which may extend to three years or with fine which may extend to five lakh rupees or with both.",
                "claim_type": "statutory",
                "topic": "hacking computer crime"
            },
            "66c": {
                "title": "Punishment for identity theft",
                "text": "Whoever, fraudulently or dishonestly make use of the electronic signature, password or any other unique identification feature of any other person, shall be punished with imprisonment of either description for a term which may extend to three years and shall also be liable to fine which may extend to rupees one lakh.",
                "claim_type": "statutory",
                "topic": "identity theft password stealing"
            },
            "66d": {
                "title": "Punishment for cheating by personation by using computer resource",
                "text": "Whoever, by means of any communication device or computer resource, cheats by personation, shall be punished with imprisonment of either description for a term which may extend to three years and shall also be liable to fine which may extend to one lakh rupees.",
                "claim_type": "statutory",
                "topic": "cyber fraud upi impersonation cheating"
            }
        }
    },
    "bharatiya nyaya sanhita, 2023": {
        "official_name": "The Bharatiya Nyaya Sanhita, 2023",
        "act_number": "Act No. 45 of 2023",
        "enactment_date": "2023-12-25",
        "commencement_date": "2024-07-01",
        "status": "in_force",
        "repealed_laws": ["Indian Penal Code, 1860"],
        "official_source": "https://www.indiacode.nic.in/handle/123456789/20042",
        "jurisdiction": "India (Central)",
        "max_section": 358,
        "sections": {
            "318": {
                "title": "Cheating",
                "text": "Whoever, by deceiving any person, fraudulently or dishonestly induces the person so deceived to deliver any property to any person... commits cheating (successor provision to IPC Section 415/420).",
                "claim_type": "statutory",
                "topic": "cheating fraud"
            },
            "318(4)": {
                "title": "Cheating and dishonestly inducing delivery of property",
                "text": "Whoever cheats and thereby dishonestly induces the person deceived to deliver any property... shall be punished with imprisonment up to seven years and fine (successor to IPC Section 420).",
                "claim_type": "statutory",
                "topic": "cheating inducement delivery of property"
            },
            "319": {
                "title": "Cheating by personation",
                "text": "A person is said to cheat by personation if he cheats by pretending to be some other person, or representing that he is a person other than he really is (successor to IPC Section 416/419).",
                "claim_type": "statutory",
                "topic": "cheating by personation fake recruiter impostor"
            },
            "75": {
                "title": "Sexual harassment",
                "text": "Unwelcome physical contact, sexually coloured remarks, or demands for sexual favours (successor to IPC Section 354A).",
                "claim_type": "statutory",
                "topic": "sexual harassment workplace"
            },
            "78": {
                "title": "Stalking",
                "text": "Following a woman or contacting her repeatedly despite disinterest, or monitoring internet/electronic communication (successor to IPC Section 354D).",
                "claim_type": "statutory",
                "topic": "cyber stalking women harassment"
            },
            "106(1)": {
                "title": "Causing death by rash or negligent act",
                "text": "Causing death of any person by doing any rash or negligent act not amounting to culpable homicide (successor to IPC Section 304A).",
                "claim_type": "statutory",
                "topic": "negligent driving death"
            },
            "125": {
                "title": "Act endangering life or personal safety of others",
                "text": "Doing any act so rashly or negligently as to endanger human life or the personal safety of others (successor to IPC Section 336/337/338).",
                "claim_type": "statutory",
                "topic": "rash act endangering safety"
            },
            "281": {
                "title": "Rash driving or riding on a public way",
                "text": "Driving any vehicle or riding on any public way in a manner so rash or negligent as to endanger human life (successor to IPC Section 279).",
                "claim_type": "statutory",
                "topic": "rash driving traffic accident"
            },
            "356": {
                "title": "Defamation",
                "text": "Whoever, by words either spoken or intended to be read, makes or publishes any imputation concerning any person intending to harm the reputation of such person (successor to IPC Section 499/500).",
                "claim_type": "statutory",
                "topic": "defamation reputation slander libel"
            },
            "316": {
                "title": "Criminal breach of trust",
                "text": "Whoever, being in any manner entrusted with property, dishonestly misappropriates or converts to his own use that property... commits criminal breach of trust (successor to IPC Section 405/406).",
                "claim_type": "statutory",
                "topic": "criminal breach of trust"
            }
        }
    },
    "indian penal code, 1860": {
        "official_name": "The Indian Penal Code, 1860",
        "act_number": "Act No. 45 of 1860",
        "enactment_date": "1860-10-06",
        "commencement_date": "1862-01-01",
        "status": "repealed",
        "repealed_by": "Bharatiya Nyaya Sanhita, 2023 (w.e.f. 1 July 2024 for prospective offences)",
        "official_source": "https://www.indiacode.nic.in/",
        "jurisdiction": "India (Central)",
        "max_section": 511,
        "sections": {
            "420": {
                "title": "Cheating and dishonestly inducing delivery of property",
                "text": "Whoever cheats and thereby dishonestly induces the person deceived to deliver any property... shall be punished with imprisonment up to seven years, and shall also be liable to fine.",
                "claim_type": "statutory",
                "topic": "cheating fraud delivery of property"
            },
            "419": {
                "title": "Punishment for cheating by personation",
                "text": "Whoever cheats by personation shall be punished with imprisonment of either description for a term which may extend to three years, or with fine, or with both.",
                "claim_type": "statutory",
                "topic": "cheating by personation impersonation"
            },
            "406": {
                "title": "Punishment for criminal breach of trust",
                "text": "Whoever commits criminal breach of trust shall be punished with imprisonment up to three years, or with fine, or with both.",
                "claim_type": "statutory",
                "topic": "criminal breach of trust"
            }
        }
    },
    "transfer of property act, 1882": {
        "official_name": "The Transfer of Property Act, 1882",
        "act_number": "Act No. 4 of 1882",
        "enactment_date": "1882-02-17",
        "commencement_date": "1882-07-01",
        "status": "in_force",
        "official_source": "https://www.indiacode.nic.in/handle/123456789/2338",
        "jurisdiction": "India (Central)",
        "max_section": 137,
        "sections": {
            "106": {
                "title": "Duration of certain leases in absence of written contract",
                "text": "In the absence of a contract or local law or usage to the contrary, a lease of immovable property for agricultural or manufacturing purposes shall be deemed to be a lease from year to year, terminable on part of either lessor or lessee, by six months' notice; and a lease of immovable property for any other purpose shall be deemed to be a lease from month to month, terminable by fifteen days' notice.",
                "claim_type": "statutory",
                "topic": "lease termination notice period 15 days"
            },
            "111": {
                "title": "Determination of lease",
                "text": "A lease of immovable property determines by lapse of time, by happening of specified event, by express surrender, by implied surrender, or by forfeiture.",
                "claim_type": "statutory",
                "topic": "determination of lease grounds"
            }
        }
    },
    "tamil nadu regulation of rights and responsibilities of landlords and tenants act, 2017": {
        "official_name": "The Tamil Nadu Regulation of Rights and Responsibilities of Landlords and Tenants Act, 2017 (TNRRLTA)",
        "act_number": "TN Act 42 of 2017",
        "enactment_date": "2017-08-04",
        "commencement_date": "2019-02-22",
        "status": "in_force",
        "repealed_laws": ["Tamil Nadu Buildings (Lease and Rent Control) Act, 1960"],
        "official_source": "https://www.indiacode.nic.in/handle/123456789/13840",
        "jurisdiction": "Tamil Nadu, India",
        "max_section": 48,
        "sections": {
            "10": {
                "title": "Security deposit",
                "text": "Save as otherwise agreed, security deposit to be paid by tenant shall not exceed three times the monthly rent. The security deposit shall be refunded to the tenant within one month of vacating the premises, after making legitimate deductions of any liabilities like unpaid rent or damages.",
                "claim_type": "statutory",
                "topic": "security deposit refund one month limit 3 months rent"
            },
            "21": {
                "title": "Application to Rent Authority / Rent Court",
                "text": "Either landlord or tenant may file an application before the Rent Authority or Rent Court for resolution of disputes relating to tenancy agreement, non-refund of deposit, or recovery of possession.",
                "claim_type": "statutory",
                "topic": "rent authority application dispute resolution"
            }
        }
    },
    "ugc regulations 2023 (student grievances)": {
        "official_name": "University Grants Commission (Redressal of Grievances of Students) Regulations, 2023",
        "act_number": "F.1-13/2022 (CPP-II)",
        "enactment_date": "2023-04-11",
        "commencement_date": "2023-04-11",
        "status": "in_force",
        "official_source": "https://www.ugc.gov.in/pdfnews/9152473_ugc-regulations-2023.pdf",
        "jurisdiction": "India (Higher Education Institutions)",
        "sections": {
            "5": {
                "title": "Student Grievance Redressal Committee (SGRC)",
                "text": "Every Collegiate Student Grievance Redressal Committee shall consider the grievances of students and send its recommendations to the Principal/Head within 15 days of receipt of grievance. Grievance includes non-refund of fees, wrongful withholding of receipts, or exam discrepancies.",
                "claim_type": "regulatory_norm",
                "topic": "student grievance committee sgrc 15 days"
            },
            "6": {
                "title": "Appointment and Role of Ombudsperson",
                "text": "Any student aggrieved by the decision of the SGRC may prefer an appeal to the Ombudsperson of the affiliating University within 15 days of receipt of decision.",
                "claim_type": "regulatory_norm",
                "topic": "ombudsperson university appeal"
            }
        }
    },
    "prevention of corruption act, 1988": {
        "official_name": "The Prevention of Corruption Act, 1988",
        "act_number": "Act No. 49 of 1988",
        "enactment_date": "1988-09-09",
        "commencement_date": "1988-09-09",
        "status": "in_force",
        "official_source": "https://www.indiacode.nic.in/handle/123456789/1947",
        "jurisdiction": "India (Central)",
        "max_section": 31,
        "sections": {
            "7": {
                "title": "Offence relating to public servant being bribed",
                "text": "Any public servant who obtains or accepts or attempts to obtain from any person, an undue advantage, with the intention to perform or cause performance of public duty improperly or dishonestly, shall be punishable with imprisonment for a term which shall not be less than three years but which may extend to seven years and shall also be liable to fine.",
                "claim_type": "statutory",
                "topic": "public servant taking bribe"
            },
            "7a": {
                "title": "Taking undue advantage to influence public servant by corrupt or illegal means",
                "text": "Whoever accepts or obtains or attempts to obtain from another person for himself or for any other person any undue advantage as a motive or reward to induce a public servant to perform improperly a public duty, shall be punishable with imprisonment for a term which shall not be less than three years but which may extend to seven years and shall also be liable to fine.",
                "claim_type": "statutory",
                "topic": "middleman taking bribe"
            },
            "13": {
                "title": "Criminal misconduct by a public servant",
                "text": "A public servant commits criminal misconduct if he dishonestly or fraudulently misappropriates or otherwise converts for his own use any property entrusted to him or intentionally enriches himself illicitly during the period of his office.",
                "claim_type": "statutory",
                "topic": "criminal misconduct corruption"
            }
        }
    },
    "right to information act, 2005": {
        "official_name": "The Right to Information Act, 2005",
        "act_number": "Act No. 22 of 2005",
        "enactment_date": "2005-06-15",
        "commencement_date": "2005-10-12",
        "status": "in_force",
        "official_source": "https://www.indiacode.nic.in/handle/123456789/2065",
        "jurisdiction": "India (Central)",
        "max_section": 31,
        "sections": {
            "6": {
                "title": "Request for obtaining information",
                "text": "A person who desires to obtain any information under this Act shall make a request in writing or through electronic means in English or Hindi or in the official language of the area accompanying prescribed fee (Rs 10) to the Central Public Information Officer (CPIO) or State Public Information Officer (SPIO).",
                "claim_type": "statutory",
                "topic": "rti application filing fee"
            },
            "7": {
                "title": "Disposal of request",
                "text": "The Central Public Information Officer or State Public Information Officer shall, as expeditiously as possible, and in any case within thirty days of the receipt of the request, either provide the information or reject the request: Provided that where the information sought for concerns the life or liberty of a person, the same shall be provided within forty-eight hours of the receipt of the request.",
                "claim_type": "statutory",
                "topic": "rti disposal deadline 30 days 48 hours"
            },
            "19": {
                "title": "Appeals",
                "text": "Any person who does not receive a decision within thirty days or is aggrieved by a decision of the PIO may within thirty days prefer an appeal to the First Appellate Authority (FAA). A second appeal against the decision shall lie within ninety days to the Central Information Commission (CIC) or State Information Commission (SIC).",
                "claim_type": "statutory",
                "topic": "rti first appeal 30 days second appeal 90 days"
            }
        }
    },
    "indian contract act, 1872": {
        "official_name": "The Indian Contract Act, 1872",
        "act_number": "Act No. 9 of 1872",
        "enactment_date": "1872-04-25",
        "commencement_date": "1872-09-01",
        "status": "in_force",
        "official_source": "https://www.indiacode.nic.in/handle/123456789/2187",
        "jurisdiction": "India (Central)",
        "max_section": 238,
        "sections": {
            "2(h)": {
                "title": "Contract definition",
                "text": "An agreement enforceable by law is a contract.",
                "claim_type": "statutory",
                "topic": "contract agreement enforceable by law"
            },
            "8": {
                "title": "Acceptance by performing conditions",
                "text": "Performance of the conditions of a proposal constitutes an acceptance of the proposal.",
                "claim_type": "statutory",
                "topic": "unilateral offer acceptance performance reward"
            },
            "73": {
                "title": "Compensation for loss or damage caused by breach of contract",
                "text": "When a contract has been broken, the party who suffers by such breach is entitled to receive from the party who has broken the contract, compensation for any loss or damage caused to him thereby.",
                "claim_type": "statutory",
                "topic": "damages breach of contract debt non-repayment"
            },
            "168": {
                "title": "Right of finder of goods; may sue for specific reward offered",
                "text": "The finder of goods has no right to sue the owner for compensation for trouble and expense voluntarily incurred by him to preserve the goods and to find the owner; but he may retain the goods until he receives such compensation; and where the owner has offered a specific reward for the return of goods lost, the finder may sue for such reward, and may retain the goods until he receives it.",
                "claim_type": "statutory",
                "topic": "finder of lost goods spectacles reward claim"
            }
        }
    },
    "motor vehicles act, 1988": {
        "official_name": "The Motor Vehicles Act, 1988",
        "act_number": "Act No. 59 of 1988",
        "enactment_date": "1988-10-14",
        "commencement_date": "1989-07-01",
        "status": "in_force",
        "official_source": "https://www.indiacode.nic.in/handle/123456789/1798",
        "jurisdiction": "India (Central)",
        "max_section": 217,
        "sections": {
            "146": {
                "title": "Necessity for insurance against third party risk",
                "text": "No person shall use, except as a passenger, or cause or allow any other person to use, a motor vehicle in a public place, unless there is in force in relation to the use of the vehicle a policy of insurance complying with statutory requirements.",
                "claim_type": "statutory",
                "topic": "mandatory third party motor insurance"
            },
            "166": {
                "title": "Application for compensation to Claims Tribunal",
                "text": "An application for compensation arising out of an accident of the nature specified in sub-section (1) of section 165 may be made by the person who has sustained the injury or by the owner of the property or legal representatives where death resulted.",
                "claim_type": "statutory",
                "topic": "mact claim application road accident compensation"
            }
        }
    },
    "sexual harassment of women at workplace act, 2013": {
        "official_name": "The Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 (POSH Act)",
        "act_number": "Act No. 14 of 2013",
        "enactment_date": "2013-04-22",
        "commencement_date": "2013-12-09",
        "status": "in_force",
        "official_source": "https://www.indiacode.nic.in/handle/123456789/2104",
        "jurisdiction": "India (Central)",
        "max_section": 30,
        "sections": {
            "4": {
                "title": "Constitution of Internal Committee",
                "text": "Every employer of a workplace shall, by an order in writing, constitute a Committee to be known as the Internal Committee (IC).",
                "claim_type": "statutory",
                "topic": "internal committee posh mandate"
            },
            "9": {
                "title": "Complaint of sexual harassment",
                "text": "Any aggrieved woman may make, in writing, a complaint of sexual harassment at workplace to the Internal Committee if so constituted, or the Local Committee, within a period of three months from the date of incident.",
                "claim_type": "statutory",
                "topic": "posh complaint 3 months limitation internal committee"
            },
            "11": {
                "title": "Inquiry into complaint",
                "text": "The Internal Committee or Local Committee shall proceed to make inquiry into the complaint in accordance with the provisions of the service rules applicable.",
                "claim_type": "statutory",
                "topic": "posh inquiry procedure"
            }
        }
    },
    "specific relief act, 1963": {
        "official_name": "The Specific Relief Act, 1963",
        "act_number": "Act No. 47 of 1963",
        "enactment_date": "1963-12-13",
        "commencement_date": "1964-03-01",
        "status": "in_force",
        "official_source": "https://www.indiacode.nic.in/handle/123456789/1583",
        "jurisdiction": "India (Central)",
        "max_section": 44,
        "sections": {
            "10": {
                "title": "Specific performance in respect of contracts",
                "text": "The specific performance of a contract shall be enforced by the court subject to the provisions contained in sub-section (2) of section 11, section 14 and section 16.",
                "claim_type": "statutory",
                "topic": "specific performance of contracts"
            },
            "38": {
                "title": "Perpetual injunction when granted",
                "text": "Subject to the other provisions contained in or referred to by this Chapter, a perpetual injunction may be granted to the plaintiff to prevent the breach of an obligation existing in his favour or invasion of right to reputation.",
                "claim_type": "statutory",
                "topic": "injunction restraining defamation"
            }
        }
    },
    "limitation act, 1963": {
        "official_name": "The Limitation Act, 1963",
        "act_number": "Act No. 36 of 1963",
        "enactment_date": "1963-10-05",
        "commencement_date": "1964-01-01",
        "status": "in_force",
        "official_source": "https://www.indiacode.nic.in/handle/123456789/1566",
        "jurisdiction": "India (Central)",
        "max_section": 32,
        "sections": {
            "article 19": {
                "title": "For money payable for money lent",
                "text": "Period of limitation is three years from the date when the loan is made.",
                "claim_type": "statutory",
                "topic": "limitation period money recovery loan 3 years"
            },
            "article 113": {
                "title": "Any suit for which no period of limitation is provided elsewhere",
                "text": "Period of limitation is three years when the right to sue accrues.",
                "claim_type": "statutory",
                "topic": "residuary limitation period 3 years"
            }
        }
    }
}


# ── Judicial Precedents & Conflicting Interpretations Registry ───────────────

JUDICIAL_PRECEDENTS: List[Dict[str, Any]] = [
    {
        "citation": "Maharshi Dayanand University v. Surjeet Kaur (2010) 11 SCC 159",
        "court": "Supreme Court of India",
        "bench": "B.S. Chauhan & Swatanter Kumar, JJ.",
        "date": "2010-07-19",
        "subject": "Education / Consumer Law",
        "holding": (
            "An educational institution or university imparting education and conducting examinations does not render "
            "a 'service' within the meaning of the Consumer Protection Act. A student is not a 'consumer'. "
            "The Consumer Forum has no jurisdiction to adjudicate disputes regarding examination admission, fee refund, or degree grant against an educational board/university."
        ),
        "conflicting_views": (
            "Conflicting/Distinguishing view: The National Consumer Disputes Redressal Commission (NCDRC) Full Bench in "
            "'Manu Solanki & Ors. v. Vinayaka Mission University' (2020) distinguished statutory education from purely commercial "
            "coaching institutes and private training centers, holding that unregulated coaching institutes DO fall under Consumer Forum jurisdiction."
        ),
        "exception_type": "Jurisdictional Exception",
        "official_source": "https://main.sci.gov.in/judgment/judis/36528.pdf"
    },
    {
        "citation": "P.T. Koshy & Anr. v. Ellen Charitable Trust & Ors. 2012 (3) CPC 615 (SC)",
        "court": "Supreme Court of India",
        "bench": "K.S. Radhakrishnan & Dipak Misra, JJ.",
        "date": "2012-08-09",
        "subject": "Education / Consumer Law",
        "holding": (
            "Educational institutions are not providing any kind of service, therefore, in the matter of admission, "
            "fees etc., there cannot be a question of deficiency of service. Such matters cannot be entertained by Consumer Forum."
        ),
        "conflicting_views": (
            "State consumer commissions sometimes admit cases if fraud, commercial misrepresentation, or purely unapproved vocational coaching is alleged."
        ),
        "exception_type": "Jurisdictional Exception",
        "official_source": "Supreme Court Special Leave to Appeal (Civil) No. 22532/2012"
    },
    {
        "citation": "Dashrath Rupsingh Rathod v. State of Maharashtra (2014) 9 SCC 129 & NI Amendment Act 2015",
        "court": "Supreme Court of India / Parliament Amendment",
        "bench": "T.S. Thakur, Vikramajit Sen & C. Nagappan, JJ.",
        "date": "2014-08-01",
        "subject": "Negotiable Instruments / Territorial Jurisdiction",
        "holding": (
            "Supreme Court held territorial jurisdiction lies where bank of drawee is situated. "
            "Parliament superseded this holding via Negotiable Instruments (Amendment) Act, 2015 (Section 142(2)), "
            "re-establishing that the complaint must be filed where the branch of the payee's bank is situated where the payee maintains the account."
        ),
        "conflicting_views": (
            "Pre-2015 judgments on jurisdiction are superseded by the statutory amendment under Section 142(2)."
        ),
        "exception_type": "Statutory Supersession",
        "official_source": "https://main.sci.gov.in/"
    },
    {
        "citation": "H.S. Goutham v. Rama Murthy (2021) 5 SCC 241",
        "court": "Supreme Court of India",
        "bench": "Ashok Bhushan & R. Subhash Reddy, JJ.",
        "date": "2021-03-08",
        "subject": "Tenancy / Security Deposit & Refund",
        "holding": (
            "Landlord cannot arbitrarily withhold tenant security deposit without proving actual damages or quantified unpaid rent. "
            "In the absence of established damage, tenant is entitled to complete refund along with interest."
        ),
        "conflicting_views": (
            "Landlord may claim set-off, but burden of proof lies strictly upon landlord to establish actual losses."
        ),
        "exception_type": "Evidentiary Burden",
        "official_source": "https://main.sci.gov.in/"
    },
    {
        "citation": "Jagmittar Sain Bhagat v. Director Health Services Haryana (2013) 10 SCC 136",
        "court": "Supreme Court of India",
        "bench": "B.S. Chauhan & S.A. Bobde, JJ.",
        "date": "2013-07-11",
        "subject": "Administrative Law / Sovereign Immunity from Consumer Protection Act",
        "holding": (
            "Government officers performing statutory or sovereign duties (such as issuing caste, income, or nativity certificates, "
            "revenue mutation, statutory licensing, or law enforcement) do not render a 'service' under Section 2(42) of the Consumer Protection Act. "
            "A statutory application fee is not commercial consideration under Section 2(7). Consumer Forums have zero jurisdiction over sovereign or statutory functions."
        ),
        "conflicting_views": (
            "Distinguished from paid commercial utility services (electricity, housing, transport) where statutory corporations act in a commercial capacity."
        ),
        "exception_type": "Sovereign Immunity Exception",
        "official_source": "https://main.sci.gov.in/"
    },
    {
        "citation": "Lucknow Development Authority v. M.K. Gupta (1994) 1 SCC 243",
        "court": "Supreme Court of India",
        "bench": "Kuldip Singh & R.M. Sahai, JJ.",
        "date": "1993-11-05",
        "subject": "Statutory Bodies / Amenability to Consumer Law for Paid Utilities",
        "holding": (
            "A government agency or statutory corporation is amenable to consumer forum jurisdiction when it renders commercial, housing, "
            "or public utility services (e.g., electricity supply by state discoms like TANGEDCO, paid municipal water tankers, or housing construction) "
            "for consideration paid by the user. Sovereign regulatory acts remain excluded."
        ),
        "conflicting_views": (
            "Sovereign and administrative certificate-issuing functions are strictly excluded from consumer forums."
        ),
        "exception_type": "Commercial Public Utility Inclusion",
        "official_source": "https://main.sci.gov.in/"
    },
    {
        "citation": "CBSE & Anr. v. Aditya Bandopadhyay & Ors. (2011) 8 SCC 497",
        "court": "Supreme Court of India",
        "bench": "R.V. Raveendran & A.K. Patnaik, JJ.",
        "date": "2011-08-09",
        "subject": "Right to Information / Scope of Section 2(f) and Section 6",
        "holding": (
            "Under the RTI Act, 2005, a citizen has the right to inspect and obtain copies of 'existing records', files, memos, and documents "
            "held by a public authority. The RTI Act does NOT require a public officer to create answers to hypothetical questions, "
            "explain 'why' a decision was taken, or generate reasons, justifications, or legal opinions not already recorded in official files."
        ),
        "conflicting_views": (
            "Citizens can obtain existing file notings and rejection orders, but cannot interrogate officers under RTI."
        ),
        "exception_type": "Statutory Scope of Information",
        "official_source": "https://main.sci.gov.in/"
    },
    {
        "citation": "Lalita Kumari v. Govt. of U.P. (2014) 2 SCC 1",
        "court": "Supreme Court of India (Constitution Bench)",
        "bench": "P. Sathasivam, C.J., B.S. Chauhan, Ranjana P. Desai, Ranjan Gogoi & S.A. Bobde, JJ.",
        "date": "2013-11-12",
        "subject": "Police Powers / Mandatory Registration of FIR",
        "holding": (
            "Registration of FIR is mandatory under Section 154 of the Code of Criminal Procedure, 1973 (and Section 173 BNSS) "
            "if the information discloses commission of a cognizable offence and no preliminary inquiry is permissible in such a situation."
        ),
        "conflicting_views": (
            "Preliminary inquiry is permissible only in exceptional cases (matrimonial, medical negligence, commercial disputes) to ascertain if cognizable offence is disclosed."
        ),
        "exception_type": "Constitution Bench Mandatory Rule",
        "official_source": "https://main.sci.gov.in/"
    },
    {
        "citation": "Hriday Ranjan Prasad Verma v. State of Bihar (2000) 4 SCC 168",
        "court": "Supreme Court of India",
        "bench": "D.P. Wadhwa & S.N. Phukan, JJ.",
        "date": "2000-03-31",
        "subject": "Breach of Contract vs Criminal Cheating",
        "holding": (
            "Distinction between mere breach of contract or failure to repay a loan and the offence of cheating "
            "depends on fraudulent intention at the inception. Subsequent failure to repay is a civil breach, not criminal cheating."
        ),
        "conflicting_views": (
            "Reaffirmed in Prof. R.K. Vijayasarathy v. Sudha Seetharam (2019) 16 SCC 739."
        ),
        "exception_type": "Civil vs Criminal Boundary Rule",
        "official_source": "https://main.sci.gov.in/"
    },
    {
        "citation": "Aureliano Fernandes v. State of Goa (2023) 14 SCC 568",
        "court": "Supreme Court of India",
        "bench": "A.S. Bopanna & Hima Kohli, JJ.",
        "date": "2023-05-12",
        "subject": "POSH Act / Mandatory Internal Committee",
        "holding": (
            "Supreme Court issued nationwide binding directives mandating strict constitution and functioning of "
            "Internal Committees (IC) under the POSH Act, 2013 across all workplaces."
        ),
        "conflicting_views": "Zero tolerance for non-compliance with statutory inquiry procedure.",
        "exception_type": "Mandatory Workplace Safeguard",
        "official_source": "https://main.sci.gov.in/"
    },
    {
        "citation": "Subramanian Swamy v. Union of India (2016) 7 SCC 221",
        "court": "Supreme Court of India",
        "bench": "Dipak Misra & Prafulla C. Pant, JJ.",
        "date": "2016-05-13",
        "subject": "Defamation / Constitutional Validity",
        "holding": (
            "Upheld constitutional validity of criminal defamation (Section 499/500 IPC / Section 356 BNS). "
            "Reaffirmed availability of civil tortious damages as a concurrent remedy."
        ),
        "conflicting_views": "Right to free speech under Article 19(1)(a) is balanced by reasonable restrictions under Article 19(2).",
        "exception_type": "Concurrent Civil & Criminal Remedy",
        "official_source": "https://main.sci.gov.in/"
    },
    {
        "citation": "National Insurance Co. Ltd. v. Pranay Sethi (2017) 16 SCC 680",
        "court": "Supreme Court of India (Constitution Bench)",
        "bench": "Dipak Misra, C.J., A.K. Sikri, A.M. Khanwilkar, D.Y. Chandrachud & Ashok Bhushan, JJ.",
        "date": "2017-10-31",
        "subject": "Motor Accident Claims / Compensation Assessment",
        "holding": (
            "Laid down standardized binding guidelines for determination of compensation before the Motor Accidents Claims Tribunal (MACT) "
            "under Section 166 of the Motor Vehicles Act, 1988."
        ),
        "conflicting_views": "Standardized conventional heads for loss of estate, consortium, and funeral expenses.",
        "exception_type": "Standardized Compensation Formula",
        "official_source": "https://main.sci.gov.in/"
    },
    {
        "citation": "Shreya Singhal v. Union of India (2015) 5 SCC 1",
        "court": "Supreme Court of India",
        "bench": "J. Chelameswar & Rohinton F. Nariman, JJ.",
        "date": "2015-03-24",
        "subject": "Information Technology / Striking Down Section 66A",
        "holding": (
            "Section 66A of the Information Technology Act, 2000 was struck down in its entirety as unconstitutional and void. "
            "Section 66A CANNOT be cited or applied to online speech or social media posts."
        ),
        "conflicting_views": "Provisions under IPC/BNS (e.g. defamation or obscenity) remain applicable.",
        "exception_type": "Constitutional Invalidity of Statutory Provision",
        "official_source": "https://main.sci.gov.in/"
    }
]


# ── Lookup and Verification Helpers ───────────────────────────────────────────

def normalize_key(name: str) -> str:
    return name.lower().replace("the ", "").replace("  ", " ").strip()


def find_statute_by_name(act_query: str) -> Optional[Dict[str, Any]]:
    q = normalize_key(act_query)
    # 1. Exact match first
    if q in STATUTES_REGISTRY:
        return STATUTES_REGISTRY[q]

    # 2. Key in query or query in key (with year priority if specified)
    candidates = []
    for key, data in STATUTES_REGISTRY.items():
        if key in q or q in key:
            candidates.append((key, data))

    if candidates:
        import re
        years = re.findall(r"\b(18\d{2}|19\d{2}|20\d{2})\b", q)
        if years:
            target_year = years[0]
            for key, data in candidates:
                if target_year in key:
                    return data
        return candidates[0][1]

    # 3. Fallback: check repealed laws
    for key, data in STATUTES_REGISTRY.items():
        if any(normalize_key(rep) in q for rep in data.get("repealed_laws", [])):
            return data

    return None


def lookup_provision(act_name: str, section_number: str) -> Optional[Dict[str, Any]]:
    statute = find_statute_by_name(act_name)
    if not statute:
        return None

    sec_clean = section_number.lower().replace("section", "").replace("sec", "").strip()
    sec_clean = sec_clean.replace("(", "").replace(")", "").strip()

    # Try exact or normalized section match
    sections = statute.get("sections", {})
    for s_key, s_data in sections.items():
        norm_key = s_key.lower().replace("(", "").replace(")", "").strip()
        if sec_clean == norm_key:
            return {
                "statute": statute,
                "section_key": s_key,
                "provision": s_data
            }

    # If section number exceeds statutory max_section
    max_sec = statute.get("max_section")
    if max_sec:
        try:
            sec_int = int(''.join(filter(str.isdigit, sec_clean)))
            if sec_int > max_sec:
                return {
                    "statute": statute,
                    "section_key": section_number,
                    "provision": None,
                    "error": f"Section {section_number} does not exist in {statute['official_name']} (Act contains only {max_sec} sections)."
                }
        except ValueError:
            pass

    return {
        "statute": statute,
        "section_key": section_number,
        "provision": None,
        "error": f"Section {section_number} not identified in verified provisions list for {statute['official_name']}."
    }


def check_temporal_validity(act_name: str, incident_date_str: Optional[str]) -> Dict[str, Any]:
    statute = find_statute_by_name(act_name)
    if not statute:
        return {"status": "unknown_act", "in_force": None, "note": "Statute not in verified database"}

    if not incident_date_str:
        return {
            "status": "date_not_provided",
            "in_force": statute.get("status") == "in_force",
            "current_status": statute.get("status"),
            "note": f"Incident date not provided. Provision is currently {statute.get('status')}."
        }

    try:
        inc_dt = datetime.fromisoformat(incident_date_str.split("T")[0])
    except Exception:
        return {
            "status": "unparseable_date",
            "in_force": None,
            "note": f"Could not parse incident date: {incident_date_str}"
        }

    commencement = datetime.fromisoformat(statute["commencement_date"])

    # Check if incident is BEFORE commencement
    if inc_dt < commencement:
        return {
            "status": "not_yet_in_force",
            "in_force": False,
            "incident_date": incident_date_str,
            "commencement_date": statute["commencement_date"],
            "note": f"{statute['official_name']} commenced on {statute['commencement_date']}. It was NOT in force on the incident date ({incident_date_str})."
        }

    # Check if Act was repealed before incident
    if statute.get("status") == "repealed":
        return {
            "status": "repealed_prior",
            "in_force": False,
            "note": f"{statute['official_name']} was repealed and cannot govern incidents post-repeal."
        }

    return {
        "status": "in_force",
        "in_force": True,
        "incident_date": incident_date_str,
        "commencement_date": statute["commencement_date"],
        "note": f"{statute['official_name']} was validly in force on {incident_date_str}."
    }


def check_education_dispute(query_text: str) -> Optional[Dict[str, Any]]:
    """
    Specifically evaluate education-related dispute rules:
    Check UGC Regulations 2023 & Supreme Court precedent
    (Surjeet Kaur, P.T. Koshy) before recommending consumer litigation.
    """
    q = query_text.lower()
    edu_keywords = ["college", "university", "school", "exam fee", "examination", "degree", "admission", "tuition", "hostel fee", "student", "ugc"]
    is_edu = any(kw in q for kw in edu_keywords)
    if not is_edu:
        return None

    return {
        "is_education_dispute": True,
        "primary_ugc_regulation": (
            "UGC (Redressal of Grievances of Students) Regulations, 2023: "
            "Mandates internal Collegiate Student Grievance Redressal Committee (SGRC) "
            "and University Ombudsperson resolution within 15 days."
        ),
        "supreme_court_precedent": (
            "Maharshi Dayanand University v. Surjeet Kaur (2010) 11 SCC 159 & P.T. Koshy v. Ellen Charitable Trust 2012 (3) CPC 615 (SC): "
            "The Supreme Court settled that educational institutions imparting education and conducting examinations do NOT provide a 'service' "
            "under the Consumer Protection Act. A student is not a 'consumer'. Consumer forum claims against statutory universities/boards risk dismissal."
        ),
        "judicial_exception": (
            "Exception (NCDRC Full Bench in Manu Solanki v. Vinayaka Mission University, 2020): "
            "Private unaccredited coaching institutes, commercial test-prep centers, and non-statutory commercial skill centers MAY be held liable under the Consumer Protection Act."
        ),
        "recommended_first_recourse": (
            "1. Formal written complaint to University Registrar & Student Grievance Redressal Committee (SGRC) under UGC 2023 Regulations.\n"
            "2. Appeal to University Ombudsperson.\n"
            "3. UGC Grievance Redressal Portal (samarth.ac.in / ugc.ac.in/grievance).\n"
            "4. Consumer Court only if coaching center/commercial unaccredited training, or Civil Suit / Writ Petition before High Court under Article 226."
        )
    }


# ── Government Service, Administrative Law & RTI Helpers ───────────────────────

def check_government_service_dispute(query_text: str, jurisdiction: str = "India") -> Optional[Dict[str, Any]]:
    """
    Evaluates whether the dispute involves a government officer, public servant,
    or administrative action, and determines the precise function type:
    - Sovereign statutory function (certificate, license, revenue mutation)
    - Paid commercial public utility (TANGEDCO electricity, water supply)
    - Corruption / bribery demand
    - Police complaint refusal
    - Right to Information (RTI)
    """
    import re
    q = query_text.lower()
    gov_keywords = [
        r"\bgovernment\b", r"\bgovt\b", r"\bofficer\b", r"\bofficial\b", r"\btahsildar\b",
        r"\brto\b", r"\bcollector\b", r"\bsub-registrar\b", r"\bbdo\b", r"\bpanchayat\b",
        r"\bmunicipality\b", r"\bcorporation\b", r"\blicense\b", r"\bdriving license\b",
        r"\bcertificate\b", r"\bcaste certificate\b", r"\bincome certificate\b",
        r"\bnativity\b", r"\bpatta\b", r"\bmutation\b", r"\bpassport\b", r"\bpublic service\b",
        r"\bbribe\b", r"\bbribery\b", r"\bcorruption\b", r"\bdvac\b", r"\bvigilance\b",
        r"\bdelay\b", r"\brefusing application\b", r"\brejected application\b",
        r"\bcitizen charter\b", r"\badministrative\b", r"\bpublic servant\b", r"\bstatutory duty\b",
        r"\btaluk\b", r"\brevenue\b", r"\bpolice\b", r"\bfir\b", r"\bsho\b", r"\bsub-inspector\b",
        r"\bpolice complaint\b", r"\badministrative complaint\b", r"\bgrievance petition\b",
        r"\bbuilding plan\b", r"\brefusing to accept\b",
        r"\brti\b", r"\bright to information\b", r"\bpio\b", r"\bpublic information officer\b",
        r"\btangedco\b", r"\bbescom\b", r"\belectricity\b", r"\bpower supply\b",
        r"\bwater tanker\b", r"\bwater connection\b", r"\bpublic utility\b"
    ]

    gov_regex = re.compile("|".join(gov_keywords), re.IGNORECASE)
    is_gov = bool(gov_regex.search(q))
    if not is_gov:
        return None

    # Subtype 1: Bribery / Corruption demand (word boundaries)
    if re.search(r"\b(bribe|bribery|undue advantage|corruption|dvac|vigilance|illegal gratification)\b", q) or "demanding money" in q:
        return {
            "is_government_dispute": True,
            "function_type": "corruption_bribery_demand",
            "cpa_applicable": False,
            "governing_statute": "The Prevention of Corruption Act, 1988 (Sections 7, 7A & 13)",
            "applicable_sections": ["Section 7", "Section 7A", "Section 13"],
            "statutory_forum": (
                "State Directorate of Vigilance and Anti-Corruption (DVAC) in Tamil Nadu (Toll-Free 1064 / https://dvac.tn.gov.in) "
                "or Central Bureau of Investigation (CBI) / Central Vigilance Commission (CVC: https://cvc.gov.in) for Central public servants."
            ),
            "prohibited_forums": [
                "Consumer Protection Act / Consumer Disputes Redressal Commission (Consumer forums have zero jurisdiction over bribery or criminal offences)."
            ],
            "legal_rationale": "Demanding or accepting an undue advantage by a public servant is a cognizable criminal offence under the Prevention of Corruption Act, 1988."
        }

    # Subtype 2: Police Refusal to register FIR / complaint (word boundaries)
    if re.search(r"\b(police|fir|sho|police station|station house officer|snatching|theft)\b", q) and any(w in q for w in ["refusing", "refuses", "register", "complaint", "station"]):
        return {
            "is_government_dispute": True,
            "function_type": "police_procedure_fir_refusal",
            "cpa_applicable": False,
            "governing_statute": "Code of Criminal Procedure, 1973 / Bharatiya Nagarik Suraksha Sanhita, 2023 & Landmark SC Rulings",
            "applicable_sections": [
                "Section 154 CrPC / Section 173 BNSS (Mandatory registration of FIR in cognizable offences)",
                "Section 154(3) CrPC / Section 173(4) BNSS (Written representation to Superintendent of Police)",
                "Section 156(3) CrPC / Section 175(3) BNSS (Application to Judicial Magistrate)",
                "Lalita Kumari v. Govt. of U.P. (2014) 2 SCC 1 (Constitution Bench SC ruling mandatory FIR)"
            ],
            "statutory_forum": "Superintendent of Police (SP/DCP) -> Judicial Magistrate under Section 156(3) CrPC / 175(3) BNSS -> Police Complaints Authority.",
            "prohibited_forums": [
                "Consumer Protection Act / Consumer Commission (Police investigation and sovereign law enforcement are strictly immune from Consumer Forum jurisdiction)."
            ],
            "legal_rationale": "Under the Constitution Bench ruling in Lalita Kumari (2014) 2 SCC 1, registration of an FIR is mandatory under Section 154 CrPC / 173 BNSS if information discloses a cognizable offence."
        }

    # Subtype 3: Paid Commercial Public Utility (e.g., TANGEDCO electricity, paid municipal water tanker)
    is_commercial_utility = any(kw in q for kw in ["electricity", "power supply", "tangedco", "bescom", "water connection", "water tanker", "railway ticket", "speed post"])
    if is_commercial_utility and any(kw in q for kw in ["bill", "excess", "tariff", "commercial", "connection", "defective meter", "paid", "inflated"]):
        return {
            "is_government_dispute": True,
            "function_type": "paid_commercial_public_utility",
            "cpa_applicable": True,
            "governing_statute": "The Consumer Protection Act, 2019 (Section 2(42), 2(7), 35) & Electricity Act, 2003",
            "applicable_sections": ["Section 2(42) CPA 2019", "Section 2(7) CPA 2019", "Section 35 CPA 2019"],
            "statutory_forum": "Consumer Disputes Redressal Commission / Electricity Consumer Grievance Redressal Forum (CGRF) & Ombudsman.",
            "prohibited_forums": [],
            "legal_rationale": "Under Lucknow Development Authority v. M.K. Gupta (1994) 1 SCC 243, when a statutory body renders commercial utility services (electricity, housing, water) for consideration, it is amenable to Consumer Protection Act jurisdiction."
        }

    # Subtype 4: RTI Application or Information Rejection (using word-boundary regex to prevent matching 'certificate')
    if re.search(r"\b(rti|right to information|pio|information officer|file notings)\b", q):
        return {
            "is_government_dispute": True,
            "function_type": "rti_application_refusal",
            "cpa_applicable": False,
            "governing_statute": "The Right to Information Act, 2005 (Sections 6, 7 & 19)",
            "applicable_sections": ["Section 6(1)", "Section 7(1)", "Section 19(1)", "Section 19(3)"],
            "statutory_forum": "Designated First Appellate Authority (FAA) -> State Information Commission (SIC) / Central Information Commission (CIC).",
            "prohibited_forums": [
                "Consumer Protection Act (RTI is an exclusive statutory regime governed by the RTI Act 2005)."
            ],
            "legal_rationale": "RTI mandates disclosure of existing public records within 30 days (or 48 hours for life and liberty). Redress lies exclusively under Section 19 appeals."
        }

    # Subtype 5: Sovereign / Statutory Administrative Function (Certificates, licenses, revenue mutation, delay)
    return {
        "is_government_dispute": True,
        "function_type": "sovereign_statutory_function",
        "cpa_applicable": False,
        "governing_statute": "State Right to Public Services Act / Citizen Charter, Departmental Statutory Rules & Article 226 of the Constitution of India",
        "applicable_sections": [
            "Right to Public Services Act / Citizen's Charter",
            "Statutory Departmental First Appeal to Superior Authority (Sub-Collector / RDO / Transport Commissioner)",
            "Article 226 of the Constitution of India (Writ of Mandamus against public officials refusing statutory duty)"
        ],
        "statutory_forum": (
            "1. Statutory First Appeal to Superior Departmental Authority (e.g., Revenue Divisional Officer (RDO) / Sub-Collector for Tahsildar; Transport Commissioner for RTO).\n"
            "2. Administrative Grievance Portals: Tamil Nadu CM Special Cell (https://cmcell.tn.gov.in) / CPGRAMS (https://pgportal.gov.in).\n"
            "3. High Court of Judicature under Article 226 for a Writ of Mandamus commanding the officer to perform their statutory duty."
        ),
        "prohibited_forums": [
            "The Consumer Protection Act, 2019 / Consumer Disputes Redressal Commission (Consumer Courts have ZERO jurisdiction over statutory certificate or license processing under Supreme Court precedent Jagmittar Sain Bhagat (2013) 10 SCC 136)."
        ],
        "legal_rationale": (
            "Under Supreme Court precedent (Jagmittar Sain Bhagat (2013) 10 SCC 136 and Secretary, Board of Secondary Education v. Santosh Kumar Sahoo), "
            "government officers performing sovereign or statutory duties (issuing caste/income/nativity certificates, licenses, or revenue records) "
            "do NOT render a 'service' under Section 2(42) of the Consumer Protection Act. A statutory fee is not commercial consideration under Section 2(7). "
            "Filing a consumer complaint against a Tahsildar or RTO for certificate or license refusal is improper and legally unsustainable."
        )
    }


def check_consumer_applicability(query_text: str, jurisdiction: str = "India") -> Dict[str, Any]:
    """
    Rigorously verifies whether the Consumer Protection Act, 2019 applies to the dispute:
    - Verifies Section 2(42) 'Service' definition.
    - Verifies Section 2(7) 'Consumer' definition.
    - Tests for sovereign/statutory immunity exclusions.
    - Distinguishes private/commercial services from government sovereign duties.
    """
    q = query_text.lower()

    # Check if this is a sovereign government duty
    gov_disp = check_government_service_dispute(query_text, jurisdiction)
    if gov_disp and not gov_disp.get("cpa_applicable", False):
        return {
            "cpa_applicable": False,
            "exclusion_reason": "Sovereign / Statutory Administrative Function",
            "applicable_statute": gov_disp.get("governing_statute"),
            "precedent_authority": "Jagmittar Sain Bhagat v. Health Services Haryana (2013) 10 SCC 136 & Santosh Kumar Sahoo",
            "notes": (
                "Consumer Protection Act 2019 is EXCLUDED. Under Section 2(42) and Supreme Court precedent, "
                "statutory certificate issuance, licensing, police functions, and sovereign duties do not constitute "
                "a 'service' rendered for commercial consideration under Section 2(7)."
            )
        }

    # Check if this is an educational institution dispute
    edu_disp = check_education_dispute(query_text)
    if edu_disp and not any(kw in q for kw in ["coaching", "unaccredited", "private commercial training"]):
        return {
            "cpa_applicable": False,
            "exclusion_reason": "Statutory Education Institution (Not a Service)",
            "applicable_statute": "UGC (Redressal of Grievances of Students) Regulations, 2023",
            "precedent_authority": "MDU v. Surjeet Kaur (2010) 11 SCC 159 & P.T. Koshy (2012)",
            "notes": "Consumer Protection Act is EXCLUDED for recognized schools, colleges, and statutory universities."
        }

    # Dispute involves private service provider or paid commercial public utility
    return {
        "cpa_applicable": True,
        "exclusion_reason": None,
        "applicable_statute": "The Consumer Protection Act, 2019",
        "precedent_authority": "Lucknow Development Authority v. M.K. Gupta (1994) 1 SCC 243",
        "notes": (
            "Consumer Protection Act 2019 is APPLICABLE under Section 2(7) (Buyer/hirer for consideration) "
            "and Section 2(42) (Commercial/utility service)."
        )
    }


def check_rti_jurisdiction(query_text: str, jurisdiction: str = "India") -> Dict[str, Any]:
    """
    Distinguishes Central versus State Government authorities for RTI queries,
    assigns the precise official portal (Tamil Nadu vs Central), explains
    Sections 6, 7 and 19, and enforces the CBSE v. Aditya Bandopadhyay limitation.
    """
    q = query_text.lower()

    # Check for Tamil Nadu State Government markers
    tn_markers = [
        "tamil nadu", "tamilnadu", "chennai", "coimbatore", "madurai", "trichy", "salem",
        "tahsildar", "taluk", "tangedco", "tn police", "district collector", "village administrative officer",
        "vao", "rdo", "state govt", "state government", "panchayat", "tn "
    ]
    is_tn = any(tm in q for tm in tn_markers) or "tamil nadu" in jurisdiction.lower()

    if is_tn:
        authority_type = "Tamil Nadu State Government Authority"
        portal_name = "Tamil Nadu RTI Online Portal"
        portal_url = "https://rtionline.tn.gov.in/"
        appeal_authority = "State Information Commission (Tamil Nadu Information Commission - TNIC)"
    else:
        authority_type = "Central Government Public Authority"
        portal_name = "RTI Online Portal (Government of India)"
        portal_url = "https://rtionline.gov.in/"
        appeal_authority = "Central Information Commission (CIC)"

    return {
        "authority_type": authority_type,
        "official_portal_name": portal_name,
        "official_portal_url": portal_url,
        "statutory_act": "The Right to Information Act, 2005",
        "sections": {
            "section_6": "Section 6(1): Application in writing or electronic mode with Rs 10 fee to the Public Information Officer (CPIO / SPIO).",
            "section_7": "Section 7(1): Mandatory disposal within 30 days (or within 48 hours where information concerns life or liberty of a person).",
            "section_19": "Section 19(1): First Appeal to designated First Appellate Authority within 30 days; Section 19(3): Second Appeal to Information Commission within 90 days."
        },
        "aditya_bandopadhyay_rule": (
            "Landmark Supreme Court Precedent (CBSE v. Aditya Bandopadhyay (2011) 8 SCC 497): "
            "Under Section 2(f) and 2(j) of the RTI Act, a citizen has the right to inspect and obtain copies of "
            "EXISTING records, files, registers, file notings, and memos held by the public authority. "
            "The RTI Act does NOT give citizens the right to demand that a public officer CREATE reasons or explanations, "
            "answer hypothetical questions, or explain 'why' an application was rejected if reasons are not already recorded in the official file."
        )
    }
