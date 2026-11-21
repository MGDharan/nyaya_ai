"""
Comprehensive Indian Legislation & Judgment Ingestion Data.
Provides full primary source texts for Central & State Legislation (Consumer, IT, NI Act, BNS, TNRRLTA, UGC).
"""

from typing import List, Dict, Any

STATUTE_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "title": "The Consumer Protection Act, 2019",
        "act_number": "Act No. 35 of 2019",
        "jurisdiction": "India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/15256",
        "text": """THE CONSUMER PROTECTION ACT, 2019
An Act to provide for protection of the interests of consumers and for the said purpose, to establish authorities for timely and effective administration and settlement of consumers' disputes.

CHAPTER I: PRELIMINARY
Section 2. Definitions.
(7) "consumer" means any person who— (i) buys any goods for a consideration which has been paid or promised or partly paid and partly promised; (ii) hires or avails of any service for a consideration. But does not include a person who obtains goods for resale or commercial purpose.
(11) "deficiency" means any fault, imperfection, shortcoming or inadequacy in the quality, nature and manner of performance which is required to be maintained by or under any law for the time being in force or has been undertaken to be performed by a person in pursuance of a contract or otherwise in relation to any service.
(42) "service" means service of any description which is made available to potential users and includes banking, financing, insurance, transport, processing, electrical supply, telecom, housing construction, entertainment.

CHAPTER IV: CONSUMER DISPUTES REDRESSAL COMMISSION
Section 34. Jurisdiction of District Commission.
(1) Subject to the other provisions of this Act, the District Commission shall have jurisdiction to entertain complaints where the value of the goods or services paid as consideration does not exceed fifty lakh rupees.
Section 35. Manner in which complaint shall be made.
(1) A complaint, in relation to any goods sold or delivered or agreed to be sold or delivered or any service provided or agreed to be provided, may be filed with a District Commission by— (a) the consumer; (b) any recognized consumer association; (c) one or more consumers having same interest.
Section 38. Procedure on admission of complaint.
(2) (a) The District Commission shall refer a copy of the admitted complaint within twenty-one days to the opposite party directing him to give his version of the case within a period of thirty days or such extended period not exceeding fifteen days as may be granted.
Section 69. Limitation period.
(1) The District Commission, the State Commission or the National Commission shall not admit a complaint unless it is filed within two years from the date on which the cause of action has arisen.
(2) A complaint may be entertained after period if complainant satisfies Commission that he had sufficient cause."""
    },
    {
        "title": "The Negotiable Instruments Act, 1881 (Cheque Bounce Provisions)",
        "act_number": "Act No. 26 of 1881",
        "jurisdiction": "India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2187",
        "text": """THE NEGOTIABLE INSTRUMENTS ACT, 1881
CHAPTER XVII: OF PENALTIES IN CASE OF DISHONOUR OF CERTAIN CHEQUES FOR INSUFFICIENCY OF FUNDS IN THE ACCOUNTS

Section 138. Dishonour of cheque for insufficiency, etc., of funds in the account.
Where any cheque drawn by a person on an account maintained by him with a banker for payment of any amount of money to another person from out of that account for the discharge, in whole or in part, of any debt or other liability, is returned by the bank unpaid, either because of the amount of money standing to the credit of that account is insufficient to honour the cheque or that it exceeds the amount arranged to be paid from that account by an agreement made with that bank, such person shall be deemed to have committed an offence and shall, without prejudice to any other provisions of this Act, be punished with imprisonment for a term which may be extended to two years, or with fine which may extend to twice the amount of the cheque, or with both:
Provided that nothing contained in this section shall apply unless—
(a) the cheque has been presented to the bank within a period of three months from the date on which it is drawn;
(b) the payee or the holder in due course of the cheque, as the case may be, makes a demand for the payment of the said amount of money by giving a notice; in writing, to the drawer of the cheque, within thirty days of the receipt of information by him from the bank regarding the return of the cheque as unpaid; and
(c) the drawer of such cheque fails to make the payment of the said amount of money to the payee or, as the case may be, to the holder in due course of the cheque, within fifteen days of the receipt of the said notice.

Section 141. Offences by companies.
(1) If the person committing an offence under section 138 is a company, every person who, at the time the offence was committed, was in charge of, and was responsible to the company for the conduct of the business of the company, as well as the company, shall be deemed to be guilty of the offence.

Section 142. Cognizance of offences.
(1) Notwithstanding anything contained in the Code of Criminal Procedure, 1973—
(a) no court shall take cognizance of any offence punishable under section 138 except upon a complaint, in writing, made by the payee;
(b) such complaint is made within one month of the date on which the cause of action arises under clause (c) of the proviso to section 138;
(2) The offence under section 138 shall be inquired into and tried only by a court within whose local jurisdiction—
(a) if the cheque is delivered for collection through an account, the branch of the bank where the payee maintains the account, is situated."""
    },
    {
        "title": "The Bharatiya Nyaya Sanhita, 2023 - Sections 318(4) & 319 (Cheating & Personation)",
        "act_number": "Act No. 45 of 2023",
        "jurisdiction": "India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/20042",
        "text": """THE BHARATIYA NYAYA SANHITA, 2023
CHAPTER XVII: OF OFFENCES AGAINST PROPERTY

Section 318. Cheating.
(4) Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.

Section 319. Cheating by personation.
(1) A person is said to cheat by personation if he cheats by pretending to be some other person, or by knowingly substituting one person for another, or representing that he or any other person is a person other than he or such other person really is.
(2) Whoever cheats by personation shall be punished with imprisonment of either description for a term which may extend to five years, or with fine, or with both."""
    },
    {
        "title": "The Information Technology Act, 2000 - Section 66D (Cheating by Personation via Computer Resource)",
        "act_number": "Act No. 21 of 2000",
        "jurisdiction": "India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1999",
        "text": """THE INFORMATION TECHNOLOGY ACT, 2000
CHAPTER XI: OFFENCES

Section 66D. Punishment for cheating by personation by using computer resource.
Whoever, by means of any communication device or computer resource cheats by personating, shall be punished with imprisonment of either description for a term which may extend to three years and shall also be liable to fine which may extend to one lakh rupees."""
    },
    {
        "title": "The Information Technology Act, 2000 - Section 66C (Identity Theft & Password Stealing)",
        "act_number": "Act No. 21 of 2000",
        "jurisdiction": "India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1999",
        "text": """THE INFORMATION TECHNOLOGY ACT, 2000
CHAPTER XI: OFFENCES

Section 66C. Punishment for identity theft.
Whoever, fraudulently or dishonestly make use of the electronic signature, password or any other unique identification feature of any other person, shall be punished with imprisonment of either description for a term which may extend to three years and shall also be liable to fine which may extend to rupees one lakh."""
    },
    {
        "title": "The Information Technology Act, 2000 - Sections 43 & 66 (Unauthorized Access, Data Damage & Hacking)",
        "act_number": "Act No. 21 of 2000",
        "jurisdiction": "India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1999",
        "text": """THE INFORMATION TECHNOLOGY ACT, 2000
CHAPTER IX: PENALTIES, COMPENSATION AND ADJUDICATION

Section 43. Penalty and compensation for damage to computer, computer system, etc.
If any person without permission of the owner or any other person who is in charge of a computer, computer system or computer network accesses, downloads, introduces computer contaminant or virus, disrupts or damages, or steals data, he shall be liable to pay damages by way of compensation to the person so affected.

CHAPTER XI: OFFENCES

Section 66. Computer related offences.
If any person, dishonestly or fraudulently, does any act referred to in section 43, he shall be punishable with imprisonment for a term which may extend to three years or with fine which may extend to five lakh rupees or with both."""
    },
    {
        "title": "UGC (Redressal of Grievances of Students) Regulations, 2023",
        "act_number": "Notification F.1-13/2022 (CPP-II)",
        "jurisdiction": "India",
        "document_type": "regulation",
        "status": "in_force",
        "source_url": "https://www.ugc.gov.in/pdfnews/9152473_ugc-regulations-2023.pdf",
        "text": """UNIVERSITY GRANTS COMMISSION (REDRESSAL OF GRIEVANCES OF STUDENTS) REGULATIONS, 2023
Gazette of India, Extraordinary, Part III, Section 4, dated 11th April, 2023.

Regulation 2. Definitions.
(g) "Grievance" means and includes complaints made on grounds of: non-refund of fee, withholding of student documents/receipts, wrongful denial of examination hall tickets, irregularities in admission process, evaluation grievances.
Regulation 5. Student Grievance Redressal Committees (SGRC).
(1) Each institution shall constitute an SGRC comprising senior faculty and student representatives.
(2) The SGRC shall send its report with recommendations to the Head of the Institution and a copy to the aggrieved student, within a period of 15 days from the date of receipt of the grievance.
Regulation 6. Appointment, Tenure and Redressal by Ombudsperson.
(1) Any student aggrieved by the decision of the SGRC may prefer an appeal to the Ombudsperson within a period of fifteen days from the date of receipt of such decision.
(2) The Ombudsperson shall hear both parties and pass a reasoned order within thirty days."""
    },
    {
        "title": "Supreme Court Landmark Rulings on Education & Consumer Jurisdiction",
        "act_number": "Judicial Precedent Digest",
        "jurisdiction": "India",
        "document_type": "judgment",
        "status": "in_force",
        "source_url": "https://main.sci.gov.in/",
        "text": """SUPREME COURT OF INDIA PRECEDENT DIGEST: EDUCATION AND CONSUMER JURISDICTION

1. Maharshi Dayanand University v. Surjeet Kaur (2010) 11 SCC 159 (Supreme Court of India):
Held: The Supreme Court held in unequivocal terms that education is not a commodity. Educational institutions imparting education and holding examinations do not render a 'service' within the meaning of the Consumer Protection Act. A student taking an examination or paying examination/tuition fee to a university is not a 'consumer'. Consequently, consumer forums have no jurisdiction to adjudicate disputes regarding examination admissions, fee refunds, or evaluation against university boards.

2. P.T. Koshy & Anr. v. Ellen Charitable Trust (2012) 3 SCC 797 (Supreme Court of India):
Reaffirmed: Educational institutions are not providing service under the Consumer Protection Act, and therefore matters relating to admission, fees, or hall tickets cannot be entertained by Consumer Forums.

3. Manu Solanki & Ors. v. Vinayaka Mission University (2020) NCDRC Full Bench:
Distinction: While statutory schools, colleges, and recognized universities are immune from consumer court complaints, unaccredited private commercial coaching centers and private training institutes providing vocational/test-preparation courses for profit DO fall within Consumer Forum jurisdiction."""
    },
    {
        "title": "Tamil Nadu Regulation of Rights and Responsibilities of Landlords and Tenants Act, 2017",
        "act_number": "TN Act No. 42 of 2017",
        "jurisdiction": "Tamil Nadu, India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/13840",
        "text": """THE TAMIL NADU REGULATION OF RIGHTS AND RESPONSIBILITIES OF LANDLORDS AND TENANTS ACT, 2017
Section 10. Security Deposit.
(1) Save as otherwise agreed to in the tenancy agreement, the security deposit to be paid by the tenant in advance shall be an amount not exceeding three months' rent for residential premises.
(2) The security deposit shall be refunded to the tenant within one month of vacating the premises and handing over possession after making legitimate deductions for unpaid rent or verified physical damages.
Section 21. Application to Rent Authority.
(1) Either landlord or tenant may file an application before the Rent Authority for determination of rent, refund of security deposit, or enforcement of tenancy rights under this Act."""
    },
    {
        "title": "Right to Information Act, 2005",
        "act_number": "Act No. 22 of 2005",
        "jurisdiction": "India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2065",
        "text": """RIGHT TO INFORMATION ACT, 2005
Section 6. Request for obtaining information.
(1) A person, who desires to obtain any information under this Act, shall make a request in writing or through electronic means in English or Hindi or in the official language of the area to the Central Public Information Officer or State Public Information Officer.
Section 7. Disposal of request.
(1) The Public Information Officer shall, as expeditiously as possible, and in any case within thirty days of the receipt of the request, either provide the information on payment of such fee as may be prescribed or reject the request for any of the reasons specified in sections 8 and 9:
Provided that where the information sought for concerns the life or liberty of a person, the same shall be provided within forty-eight hours of the receipt of the request.
Section 19. Appeal.
(1) Any person who does not receive a decision within the time specified or is aggrieved by a decision may prefer a First Appeal within thirty days to the First Appellate Authority.
(3) A Second Appeal against the decision shall lie within ninety days to the Central Information Commission or State Information Commission."""
    },
    {
        "title": "Payment of Wages Act, 1936 & Industrial Disputes Act, 1947 (Unpaid Salary Claims)",
        "act_number": "Labour Laws Digest",
        "jurisdiction": "India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2361",
        "text": """LABOUR & EMPLOYMENT LEGISLATION: SALARY RECOVERY
Payment of Wages Act, 1936 - Section 15. Claims arising out of deductions from wages or delay in payment of wages.
(1) The appropriate Government may appoint an Authority to hear and decide for any specified area all claims arising out of deductions from or delay in payment of wages of persons employed.
(2) Where contrary to the provisions of this Act any deduction has been made or delay in payment has occurred, an application may be made by the employed person within twelve months.
Industrial Disputes Act, 1947 - Section 33C. Recovery of money due from an employer.
(2) Where any workman is entitled to receive from the employer any money or any benefit which is capable of being computed in terms of money, the Labour Court may specify the amount due and issue recovery certificates."""
    },
    {
        "title": "Maternity Benefit Act, 1961 (as amended by Maternity Benefit Amendment Act, 2017)",
        "act_number": "Act No. 53 of 1961",
        "jurisdiction": "India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1681",
        "text": """THE MATERNITY BENEFIT ACT, 1961
Section 5. Right to payment of maternity benefit.
(1) Subject to the provisions of this Act, every woman shall be entitled to, and her employer shall be liable for, the payment of maternity benefit at the rate of the average daily wage for the period of her actual absence.
(3) The maximum period for which any woman shall be entitled to maternity benefit shall be twenty-six weeks of which not more than eight weeks shall precede the date of her expected delivery.
Section 12. Dismissal during absence of pregnancy.
(1) When a woman absents herself from work in accordance with the provisions of this Act, it shall be unlawful for her employer to discharge or dismiss her during or on account of such absence, or to give notice of discharge or dismissal on such a day that the notice will expire during such absence."""
    },
    {
        "title": "Police Procedures, Cognizable Offences & Mandatory FIR Registration",
        "act_number": "Criminal Procedure Digest",
        "jurisdiction": "India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://main.sci.gov.in/",
        "text": """MANDATORY FIR REGISTRATION & MAGISTRATE POWERS
1. Lalita Kumari v. Govt. of U.P. (2014) 2 SCC 1 (Constitution Bench Supreme Court of India):
Held: Registration of FIR is mandatory under Section 154 of the Code of Criminal Procedure, 1973 (and Section 173 BNSS) if the information discloses commission of a cognizable offence and no preliminary inquiry is permissible in such a situation.
2. Section 154 CrPC / Section 173 Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023:
Information in cognizable cases. Every information relating to the commission of a cognizable offence shall be reduced to writing by the officer in charge of a police station and entered in a book to be kept by such officer.
3. Section 156(3) CrPC / Section 175(3) BNSS, 2023:
Any Magistrate empowered under section 190 may order such an investigation to be made by the police in the event police refuse to register an FIR."""
    },
    {
        "title": "Cyber Harassment, Voyeurism & Information Technology Act Provisions",
        "act_number": "Cyber Law Digest",
        "jurisdiction": "India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1999",
        "text": """CYBER HARASSMENT, VOYEURISM & PRIVACY VIOLATIONS
Information Technology Act, 2000 - Section 66E. Punishment for violation of privacy.
Whoever, intentionally or knowingly captures, publishes or transmits the image of a private area of any person without his or her consent, shall be punished with imprisonment up to three years or fine up to two lakh rupees.
Information Technology Act, 2000 - Section 67 & 67A.
Punishment for publishing or transmitting obscene material or material containing sexually explicit act in electronic form with imprisonment extending up to five years.
Indian Penal Code Section 354D / Bharatiya Nyaya Sanhita Section 78: Stalking online or monitoring women's electronic communication.
Indian Penal Code Section 509 / Bharatiya Nyaya Sanhita Section 79: Word, gesture or act intended to insult modesty of woman."""
    },
    {
        "title": "Consumer Protection (E-Commerce) Rules, 2020 & CPA E-Commerce Liability",
        "act_number": "G.S.R. 462(E)",
        "jurisdiction": "India",
        "document_type": "regulation",
        "status": "in_force",
        "source_url": "https://consumeraffairs.nic.in/",
        "text": """CONSUMER PROTECTION (E-COMMERCE) RULES, 2020
Rule 4. Duties of e-commerce entities.
(1) Every e-commerce entity shall establish an adequate grievance redressal mechanism and appoint a grievance officer for consumer grievance redressal.
(2) Grievance officer shall acknowledge the receipt of any consumer complaint within forty-eight hours and redress the complaint within one month from the date of receipt of the complaint.
Rule 5. Liabilities of marketplace e-commerce entities.
(3) No marketplace e-commerce entity shall impose cancellation fees on consumers after confirming purchase unless similar charges are also borne by the e-commerce entity if they cancel the purchase order unilaterally.
Section 35 Consumer Protection Act, 2019: Consumer may file complaint electronically through e-Daakhil portal for deficiency of service or defective goods."""
    },
    {
        "title": "Reserve Bank of India Circular on Customer Protection: Limiting Liability in Electronic Banking Transactions",
        "act_number": "RBI/2017-18/15 DBR.No.Leg.BC.78/09.07.005/2017-18",
        "jurisdiction": "India",
        "document_type": "circular",
        "status": "in_force",
        "source_url": "https://www.rbi.org.in/",
        "text": """RESERVE BANK OF INDIA: CUSTOMER PROTECTION - LIMITING LIABILITY IN UNAUTHORIZED ELECTRONIC TRANSACTIONS
Paragraph 6. Zero Liability of a Customer:
A customer's entitlement to zero liability shall arise where the unauthorised transaction occurs in the following events:
(a) Contributory fraud/negligence/deficiency on the part of the bank (irrespective of whether or not the transaction is reported by the customer).
(b) Third party breach where the deficiency lies neither with the bank nor with the customer but lies elsewhere in the system, and the customer notifies the bank within three working days of receiving the communication from the bank regarding the unauthorised transaction.
Paragraph 7. Limited Liability of a Customer:
Where the loss is due to negligence by a customer, such as where he has shared the payment credentials, the customer will bear the entire loss until he reports the unauthorised transaction to the bank."""
    },
    {
        "title": "Statutory Maintenance for Wife and Children (CrPC 125 / BNSS 144 & DV Act)",
        "act_number": "Family Law Digest",
        "jurisdiction": "India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2263",
        "text": """MAINTENANCE UNDER INDIAN LAW: SECTION 125 CrPC / SECTION 144 BNSS & DV ACT
Section 125 Code of Criminal Procedure, 1973 / Section 144 Bharatiya Nagarik Suraksha Sanhita (BNSS), 2023:
Order for maintenance of wives, children and parents. If any person having sufficient means neglects or refuses to maintain his wife, unable to maintain herself, or legitimate/illegitimate minor child, a Magistrate of the first class may order such person to make a monthly allowance for maintenance.
Interim Maintenance: During the pendency of the proceeding, the Magistrate may order interim monthly maintenance.
Protection of Women from Domestic Violence Act, 2005 - Section 20 & Section 23:
Monetary reliefs and ex-parte interim maintenance orders to protect women and minor children.
Supreme Court Landmark Precedent: Rajnesh v. Neha (2020) 2 SCC 324:
Mandated filing of comprehensive Affidavits of Assets and Liabilities by both parties at the initial stage to ensure prompt grant of interim maintenance without awaiting protracted trial."""
    },
    {
        "title": "Temporal Application of Criminal Laws & Article 20(1) Constitution of India",
        "act_number": "Constitutional & Penal Law Digest",
        "jurisdiction": "India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2187",
        "text": """TEMPORAL APPLICATION OF CRIMINAL LAWS & CONSTITUTIONAL MANDATE
Article 20(1) of the Constitution of India:
Protection in respect of conviction for offences. No person shall be convicted of any offence except for violation of a law in force at the time of the commission of the act charged as an offence, nor be subjected to a penalty greater than that which might have been inflicted under the law in force at the time of the commission of the offence.
Substantive Law Commencement Rule:
1. Bharatiya Nyaya Sanhita, 2023 (BNS) came into force on 1 July 2024.
2. For any offence committed PRIOR to 1 July 2024, the substantive offence MUST be registered and charged under the Indian Penal Code, 1860 (IPC). Applying BNS 2023 to pre-July 2024 acts violates Article 20(1) of the Constitution.
3. For offences committed on or after 1 July 2024, the substantive charges must be under the Bharatiya Nyaya Sanhita, 2023."""
    },
    {
        "title": "Civil Recovery Procedure, Summary Suits & Criminal Fraud (CPC Order 37 & IPC 420 / BNS 318)",
        "act_number": "Civil & Criminal Recovery Digest",
        "jurisdiction": "India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2191",
        "text": """LEGAL MECHANISMS FOR RECOVERY OF MONEY
1. Code of Civil Procedure, 1908 - Order XXXVII (Summary Suits):
Allows expedited recovery of debts arising on written contracts, promissory notes, bills of exchange, or cheques, where the defendant is not entitled to defend as a matter of right without obtaining leave from the court.
2. Bharatiya Nyaya Sanhita Section 318 / Indian Penal Code Section 420 (Cheating and dishonestly inducing delivery of property):
Applicable where there was dishonest or fraudulent intention from the inception of the transaction.
3. Section 138 Negotiable Instruments Act, 1881:
Applicable where payment was made or debt was acknowledged via cheque that was subsequently dishonoured for insufficient funds."""
    },
    {
        "title": "The Prevention of Corruption Act, 1988 (Bribery & Corruption Provisions)",
        "act_number": "Act No. 49 of 1988",
        "jurisdiction": "India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/1947",
        "text": """THE PREVENTION OF CORRUPTION ACT, 1988
Section 7. Offence relating to public servant being bribed.
Any public servant who obtains or accepts or attempts to obtain from any person, an undue advantage, with the intention to perform or cause performance of public duty improperly or dishonestly, shall be punishable with imprisonment for a term which shall not be less than three years but which may extend to seven years and shall also be liable to fine.
Section 7A. Taking undue advantage to influence public servant by corrupt or illegal means.
Whoever accepts or obtains or attempts to obtain from another person for himself or for any other person any undue advantage as a motive or reward to induce a public servant to perform improperly a public duty, shall be punishable with imprisonment for a term which shall not be less than three years but which may extend to seven years and shall also be liable to fine.
Section 13. Criminal misconduct by a public servant.
A public servant commits criminal misconduct if he dishonestly or fraudulently misappropriates or converts for his own use any property entrusted to him or intentionally enriches himself illicitly.
Complaint Authority: Directorate of Vigilance and Anti-Corruption (DVAC) in Tamil Nadu (Toll-Free 1064 / https://dvac.tn.gov.in) or Central Vigilance Commission (CVC) / CBI for Central public servants."""
    },
    {
        "title": "Sovereign Statutory Functions & Administrative Immunity Digest (Supreme Court of India)",
        "act_number": "Administrative Law Digest",
        "jurisdiction": "India",
        "document_type": "judgment",
        "status": "in_force",
        "source_url": "https://main.sci.gov.in/",
        "text": """SUPREME COURT LANDMARK HOLDINGS: SOVEREIGN DUTIES VS CONSUMER LAW
1. Jagmittar Sain Bhagat v. Health Services Haryana (2013) 10 SCC 136:
Held: Government servants and public functionaries performing sovereign or statutory duties (such as issuing government certificates, revenue mutation, statutory licensing, or law enforcement) do not render a 'service' under Section 2(42) of the Consumer Protection Act. A statutory application fee is not commercial consideration under Section 2(7). Consumer Forums have zero jurisdiction over sovereign or statutory functions.
2. Secretary, Board of Secondary Education v. Santosh Kumar Sahoo & Bihar School Examination Board:
Reaffirmed: Statutory authorities discharging public administrative or regulatory duties are immune from Consumer Protection Act complaints. Statutory fees cannot be equated with consideration for hiring a service.
3. Lucknow Development Authority v. M.K. Gupta (1994) 1 SCC 243:
Distinction: While purely sovereign regulatory duties are excluded, a government body or statutory corporation is amenable to consumer forum jurisdiction when it renders commercial, housing, or public utility services (such as electricity distribution by TANGEDCO, paid municipal water tankers, or commercial transport) for consideration.
4. Article 226 of the Constitution of India (Writ of Mandamus):
Constitutional remedy against arbitrary refusal or inaction by a public officer. A High Court can issue a Writ of Mandamus commanding the public authority to perform their mandatory statutory duty without delay."""
    },
    {
        "title": "Right to Information Act, 2005 (Sections 6, 7, 19 & Aditya Bandopadhyay Precedent)",
        "act_number": "Act No. 22 of 2005",
        "jurisdiction": "India",
        "document_type": "statute",
        "status": "in_force",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/2065",
        "text": """RIGHT TO INFORMATION ACT, 2005 & JURISDICTIONAL PORTALS
Section 6. Request for obtaining information.
(1) An applicant may submit a written or electronic request with the prescribed fee (Rs 10) to the Central/State Public Information Officer.
Section 7. Disposal of request.
(1) Mandatory response within 30 days of receipt; provided that where the information concerns the life or liberty of a person, it shall be provided within 48 hours.
Section 19. Appeals.
(1) First Appeal lies within 30 days to the First Appellate Authority (FAA).
(3) Second Appeal lies within 90 days to the State Information Commission (SIC) or Central Information Commission (CIC).
Portals:
- Tamil Nadu State Public Authorities: https://rtionline.tn.gov.in/
- Central Government Public Authorities: https://rtionline.gov.in/
Landmark Precedent (CBSE v. Aditya Bandopadhyay (2011) 8 SCC 497):
The right under RTI is confined to seeking disclosure of EXISTING records, file notings, orders, and memos held by a public authority. Citizens cannot use RTI to demand that a public officer create reasons, answer hypothetical questions, or explain 'why' a decision was taken if not recorded in files."""
    },
    {
        "title": "Public Services Delivery, Citizen Charters & Administrative Grievance Portals",
        "act_number": "Public Service Guarantee Digest",
        "jurisdiction": "India & Tamil Nadu",
        "document_type": "regulation",
        "status": "in_force",
        "source_url": "https://pgportal.gov.in/",
        "text": """PUBLIC SERVICES GUARANTEE & ADMINISTRATIVE GRIEVANCE REDRESSAL
1. Statutory Citizen Charter & Right to Public Services Framework:
Mandates designated service delivery timelines for government certificates (caste, income, nativity certificates), revenue mutations, driving licenses, and permits.
2. Departmental Hierarchy & Administrative First Appeal:
Aggrieved citizen must prefer a departmental First Appeal to the designated superior officer (e.g. Revenue Divisional Officer (RDO) / Sub-Collector for Tahsildar; Transport Commissioner for RTO).
3. Online Administrative Grievance Portals:
- Central Government Authorities: CPGRAMS (Centralised Public Grievance Redress and Monitoring System: https://pgportal.gov.in)
- Tamil Nadu State Authorities: CM Special Cell (https://cmcell.tn.gov.in) / TN e-Sevai Portal (https://tnesevai.tn.gov.in)
4. Judicial Recourse:
Filing a Writ Petition under Article 226 of the Constitution of India before the High Court for a Writ of Mandamus."""
    }
]
