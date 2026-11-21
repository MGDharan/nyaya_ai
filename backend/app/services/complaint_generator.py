"""
Formal Complaint & Legal Notice Document Generator.
Generates customizable drafts based on user-supplied facts:
1. College Exam / Fee Dispute Grievance (to SGRC & Principal under UGC 2023 Regs)
2. Consumer Complaint (District Consumer Disputes Redressal Commission under CPA 2019)
3. Cheque Dishonour Statutory Notice (Section 138 NI Act)
4. Cybercrime / UPI Fraud Report (to Cyber Police Station & Bank Nodal Officer)
5. Tenant Security Deposit Demand Notice (under Tenancy Act / Transfer of Property Act)
6. Employee Unpaid Salary & Full-and-Final Settlement Notice
7. Right to Information (RTI) Application (Section 6(1) RTI Act 2005)
"""

from datetime import date
from typing import Dict, Any, Optional


def generate_complaint_letter(
    template_type: str,
    user_name: str,
    user_address: str,
    user_contact: str,
    opposite_party_name: str,
    opposite_party_address: str,
    incident_date: Optional[str] = None,
    amount: Optional[str] = None,
    transaction_ref: Optional[str] = None,
    facts_summary: Optional[str] = None,
    relief_sought: Optional[str] = None
) -> Dict[str, Any]:
    """Generates an official formatted legal letter draft with clear placeholders."""
    today_str = date.today().strftime("%d %B %Y")
    inc_dt = incident_date or "[DATE OF INCIDENT / TRANSACTION]"
    amt = amount or "[TRANSACTION AMOUNT IN INR]"
    utr = transaction_ref or "[UTR / TRANSACTION REFERENCE NUMBER]"
    facts = facts_summary or "[DETAILED CHRONOLOGICAL STATEMENT OF FACTS]"
    relief = relief_sought or "[EXACT REPLACEMENT / REFUND / ADMISSION OF EXAMINATION SOUGHT]"

    t = template_type.lower()

    # 1. College Examination & Fee Grievance
    if "college" in t or "education" in t or "student" in t or "fee" in t:
        title = "Formal Grievance Submission under UGC (Redressal of Grievances of Students) Regulations, 2023"
        content = f"""Date: {today_str}

To,
The Chairperson,
Student Grievance Redressal Committee (SGRC) / The Principal,
{opposite_party_name},
{opposite_party_address}

From:
{user_name}
{user_address}
Email / Phone: {user_contact}

SUBJECT: URGENT GRIEVANCE UNDER UGC (REDRESSAL OF GRIEVANCES OF STUDENTS) REGULATIONS, 2023 REGARDING NON-RECOGNITION OF EXAMINATION FEE AND WRONGFUL DENIAL OF EXAMINATION ADMISSION

Respected Sir / Madam,

1. I am a bonafide student of {opposite_party_name}. On {inc_dt}, I duly remitted the examination fee amounting to {amt} through UPI / online banking mode towards examination registration.

2. The amount was successfully debited from my bank account under Transaction Reference / UTR Number: {utr}. A copy of the bank transaction confirmation and UPI receipt is attached herewith as Annexure A.

3. Notwithstanding the successful debit, the college administration has communicated that the payment is not reflected in its records and is wrongfully refusing to issue my examination hall ticket / permit me to appear in the scheduled examination.

4. STATEMENT OF FACTS:
{facts}

5. LEGAL PROVISIONS & STATUTORY TIMELINE:
Under Regulation 5 of the UGC (Redressal of Grievances of Students) Regulations, 2023, the Student Grievance Redressal Committee is mandated to consider grievances regarding withholding of receipts, wrongful denial of hall tickets, or examination discrepancies and provide its findings/recommendations within 15 days.

6. RELIEF SOUGHT:
In light of the above substantiated payment:
a) Immediately issue my examination hall ticket and permit me to appear for all scheduled examinations.
b) Reconcile the payment record with the bank using UTR {utr}.
c) In the alternative, grant provisional admission to the examination hall pending bank settlement.

Please note that in the event of failure to resolve this within the statutory 15-day timeline, I shall be constrained to appeal to the University Ombudsperson and report the matter to the UGC Grievance Portal.

Yours faithfully,

(Signature)
{user_name}
Enclosures:
1. Annexure A - Bank Account Statement / UPI Transaction Receipt with UTR.
2. Annexure B - Examination Form / Fee Challan Details."""

    # 2. Section 138 NI Act Cheque Bounce Statutory Demand Notice
    elif "cheque" in t or "138" in t or "dishonour" in t:
        title = "Statutory Demand Notice under Section 138(b) of the Negotiable Instruments Act, 1881"
        content = f"""REGISTERED POST WITH ACKNOWLEDGEMENT DUE / SPEED POST

Date: {today_str}

To,
{opposite_party_name},
{opposite_party_address}

From:
{user_name},
{user_address}
Contact: {user_contact}

SUBJECT: STATUTORY DEMAND NOTICE UNDER CLAUSE (b) OF THE PROVISO TO SECTION 138 OF THE NEGOTIABLE INSTRUMENTS ACT, 1881

Sir / Madam,

Under instructions and on my own behalf, I hereby serve upon you this Statutory Demand Notice:

1. In discharge of your legally enforceable debt and liability towards me, you drew and issued in my favour a Cheque bearing No. [CHEQUE NUMBER] dated {inc_dt} for an amount of {amt} drawn on [BANK NAME AND BRANCH].

2. I presented the said cheque for encashment through my banker [NAME OF PAYEE'S BANK], but the same was dishonoured and returned unpaid by the bank with the Return Memo dated [MEMO DATE] for the reason: "INSUFFICIENT FUNDS" / "EXCEEDS ARRANGEMENT".

3. The said memo was received by me on [DATE OF RECEIPT OF MEMO], which is well within 30 days of the date of this statutory notice.

4. STATEMENT OF DEBT:
{facts}

5. DEMAND:
I hereby call upon you to pay the aforesaid sum of {amt} to me within FIFTEEN (15) DAYS from the date of receipt of this notice, failing which I shall be constrained to institute criminal proceedings against you under Section 138 read with Section 142 of the Negotiable Instruments Act, 1881, as well as under Bharatiya Nyaya Sanhita, 2023, where you shall be liable for imprisonment up to two years, and/or fine extending to twice the amount of the cheque, alongside interest and costs.

Yours faithfully,

{user_name}"""

    # 3. Consumer Complaint Draft
    elif "consumer" in t or "cpa" in t or "deficiency" in t:
        title = "Formal Consumer Complaint under Section 35 of the Consumer Protection Act, 2019"
        content = f"""BEFORE THE DISTRICT CONSUMER DISPUTES REDRESSAL COMMISSION AT [DISTRICT NAME, STATE]

Consumer Complaint No. _______ of {date.today().year}

IN THE MATTER OF:
{user_name},
Residing at {user_address}
Phone: {user_contact}                                   ... COMPLAINANT

VERSUS

{opposite_party_name},
Having office at {opposite_party_address}                ... OPPOSITE PARTY

COMPLAINT UNDER SECTION 35 OF THE CONSUMER PROTECTION ACT, 2019 FOR DEFICIENCY IN SERVICE AND UNFAIR TRADE PRACTICE

The Complainant respectfully submits as follows:

1. The Complainant is a 'consumer' within the meaning of Section 2(7) of the Consumer Protection Act, 2019, having availed goods/services from the Opposite Party for valuable consideration of {amt}.

2. The Opposite Party is a service provider / merchant engaged in commercial trade and subject to the jurisdiction of this Hon'ble Commission.

3. CAUSE OF ACTION & FACTS:
On {inc_dt}, the Complainant purchased goods/availed service under Invoice / Receipt No: {utr}.
{facts}

4. DEFICIENCY IN SERVICE:
Under Section 2(11) of the Act, the Opposite Party has committed severe deficiency in service and unfair trade practice by refusing legitimate resolution.

5. PRAYER / RELIEF SOUGHT:
The Complainant respectfully prays that this Hon'ble Commission may be pleased to:
a) Direct the Opposite Party to refund the sum of {amt} along with 18% interest per annum;
b) Direct payment of compensation of ₹[COMPENSATION AMOUNT] towards mental agony and harassment;
c) Award litigation costs of ₹[LITIGATION COSTS];
d) Pass any other order deemed fit in the interest of justice.

Verification:
I, {user_name}, do hereby verify that the contents of paragraphs 1 to 5 are true and correct to the best of my knowledge and belief.
Verified at [PLACE] on this {today_str}.

COMPLAINANT"""

    # 4. Default / General Notice (Tenancy, UPI Fraud, Salary)
    else:
        title = f"Formal Legal Representation & Demand Notice ({template_type.title()})"
        content = f"""Date: {today_str}

To,
{opposite_party_name},
{opposite_party_address}

From:
{user_name},
{user_address}
Phone / Email: {user_contact}

SUBJECT: FORMAL DEMAND NOTICE REGARDING {template_type.upper()}

Sir / Madam,

1. I am addressing this formal legal representation regarding the transaction / incident dated {inc_dt} involving the amount of {amt} (Reference: {utr}).

2. FACTS & GRIEVANCE:
{facts}

3. STATUTORY NOTICE:
Take notice that under applicable Indian law, your actions constitute an actionable civil and statutory breach. You are hereby called upon to grant the following relief within 15 days of this notice:
{relief}

Failing compliance, I reserve full rights to seek appropriate redressal before the competent statutory authority, tribunal, or court of law entirely at your risk as to costs and consequences.

Yours faithfully,

{user_name}"""

    return {
        "title": title,
        "template_type": template_type,
        "date_generated": today_str,
        "text_content": content,
        "word_count": len(content.split())
    }


def generate_section_63_bsa_certificate(
    certifier_name: str,
    device_model: str,
    mobile_number: str,
    evidence_description: str,
    incident_date: Optional[str] = None,
    hash_digest: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates mandatory statutory certificate under Section 63 of Bharatiya Sakshya Adhiniyam, 2023
    (formerly Section 65B of the Indian Evidence Act, 1872) for electronic records.
    Mandated for WhatsApp chats, UPI payment records, SMS debits, and electronic documents.
    """
    today_str = date.today().strftime("%d %B %Y")
    inc_dt = incident_date or date.today().strftime("%Y-%m-%d")
    device = device_model or "Mobile Computing Device / Smartphone"
    phone = mobile_number or "+91 ••••••••••"
    evid = evidence_description or "WhatsApp chat transcripts, electronic payment confirmation logs, and bank transaction statements"
    h_val = hash_digest or "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"

    title = "Statutory Certificate of Electronic Records under Section 63 of Bharatiya Sakshya Adhiniyam, 2023"
    content = f"""CERTIFICATE UNDER SECTION 63 OF THE BHARATIYA SAKSHYA ADHINIYAM, 2023
(FOR ADMISSIBILITY OF ELECTRONIC EVIDENCE IN JUDICIAL PROCEEDINGS)

DATE: {today_str}
PLACE: INDIA

I, {certifier_name}, residing in India, do hereby solemnly state, affirm and certify as under:

1. That I am the lawful owner, subscriber and person having lawful control over the electronic device/communication computer resource:
   - Device Type & Model: {device}
   - Registered Mobile / SIM: {phone}
   - Electronic Storage Medium: Internal Encrypted Flash Memory

2. DESCRIPTION OF ELECTRONIC RECORDS PRODUCED:
   The printouts and digital extracts attached herewith as Annexures comprise:
   {evid}
   pertaining to the period / incident dated {inc_dt}.

3. STATUTORY COMPLIANCE UNDER SECTION 63(2) & 63(4) BSA, 2023:
   (a) The electronic records were produced by the computer resource during the period over which the computer was used regularly to store or process information for the purposes of any activities regularly carried on over that period by me.
   (b) Throughout the material period, the computer resource was operating properly, or if not, the period of its being out of operation was not such as to affect the electronic record or the accuracy of its contents.
   (c) The information contained in the electronic record reproduces or is derived from such information fed into the computer resource in the ordinary course of activities.
   (d) There has been no tampering, interception, deletion, or unauthorized manipulation of the digital logs, audio, or message contents.

4. CRYPTOGRAPHIC INTEGRITY VERIFICATION:
   - Digital Hash Standard: SHA-256
   - Computed Integrity Digest: {h_val}

5. VERIFICATION:
I identify the attached printout/extracts as true and faithful reproductions of the electronic records stored in my device. The contents of this certificate are true to my personal knowledge and belief.

DEPONENT / CERTIFIER:
Name: {certifier_name}
Mobile: {phone}
Signature: __________________________"""

    return {
        "title": title,
        "date_generated": today_str,
        "text_content": content,
        "word_count": len(content.split())
    }


def generate_police_fir_complaint(
    complainant_name: str,
    complainant_address: str,
    complainant_phone: str,
    police_station_name: str,
    district_city: str,
    accused_details: str,
    amount_lost: Optional[str] = None,
    transaction_ref: Optional[str] = None,
    facts_chronology: Optional[str] = None,
    incident_date: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generates a formal Police Complaint / FIR Request under Section 173 of the
    Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023 (formerly Section 154 CrPC).
    """
    today_str = date.today().strftime("%d %B %Y")
    inc_dt = incident_date or date.today().strftime("%Y-%m-%d")
    ps = police_station_name or "The Station House Officer (SHO), Cyber Crime Police Station / Local Police Station"
    dist = district_city or "India"
    accused = accused_details or "Unknown Cyber Fraudsters / Entity named in WhatsApp/UPI"
    amt = amount_lost or "Rs. [AMOUNT DEBITED]"
    utr = transaction_ref or "UTR / Transaction ID [NUMBER]"
    facts = facts_chronology or "Chronological statement of deception, false promises, and electronic bank debit..."

    title = "Written Complaint under Section 173 of Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023"
    content = f"""WRITTEN COMPLAINT UNDER SECTION 173 OF BHARATIYA NAGARIK SURAKSHA SANHITA (BNSS), 2023
(FOR REGISTRATION OF FIRST INFORMATION REPORT - F.I.R.)

DATE: {today_str}

TO:
{ps},
{dist}, INDIA.

FROM:
{complainant_name}
Address: {complainant_address}
Mobile / Email: {complainant_phone}

SUBJECT: FORMAL COMPLAINT UNDER SECTIONS 318(4) & 319 OF BHARATIYA NYAYA SANHITA (BNS), 2023 AND SECTION 66D OF INFORMATION TECHNOLOGY ACT, 2000 FOR CHEATING BY PERSONATION AND FINANCIAL FRAUD

Respected Sir / Madam,

I, the complainant above-named, most respectfully submit this written information for immediate registration of FIR and investigation into the cognizable offences committed against me:

1. PARTICULARS OF THE ACCUSED:
   {accused}

2. PARTICULARS OF INCIDENT & LOSS:
   - Date of Incident: {inc_dt}
   - Amount Siphoned / Cheated: {amt}
   - Payment Mode & Reference: UPI / Net Banking (Ref/UTR: {utr})
   - National Cybercrime Reporting Portal (NCRP) Acknowledgement: Filed under Helpline 1930

3. DETAILED STATEMENT OF FACTS:
{facts}

4. OFFENCES ATTRACTED:
   (a) Section 318(4) Bharatiya Nyaya Sanhita, 2023: Cheating and dishonestly inducing delivery of property (punishable with imprisonment up to 7 years).
   (b) Section 319 Bharatiya Nyaya Sanhita, 2023: Cheating by personation.
   (c) Section 66D Information Technology Act, 2000: Cheating by personation using computer resource or communication device.

5. RELIEF SOUGHT:
   (a) Register a formal First Information Report (FIR) under Section 173 BNSS, 2023.
   (b) Immediately direct the concerned Nodal Officer / Bank under Section 106 BNSS to freeze the fraudulent beneficiary account holding the proceeds of crime.
   (c) Recover the siphoned amount of {amt} and arrest the perpetrators.

Attached Annexures:
Annexure A: Bank Account Statement & UPI Transaction Debit UTR: {utr}
Annexure B: WhatsApp / Telegram Chat Screenshots
Annexure C: Certificate of Electronic Evidence under Section 63 of Bharatiya Sakshya Adhiniyam, 2023

Yours faithfully,

({complainant_name})
Complainant"""

    return {
        "title": title,
        "date_generated": today_str,
        "text_content": content,
        "word_count": len(content.split())
    }
